import matplotlib.pyplot as plt
import numpy as np 
from math import *
from pylab import *
from random import *
from os import chdir,getcwd,mkdir 
import matplotlib.image as mpimg
import matplotlib.animation as animation
import time
import sqlite3
import time

#Petite info :Pyzo affiche un message lorsque l'on lance le programme qui nous dit que la méthode pour rafraichir l'écran, qui utilise plt.clf() +plt.pause(0.0001) n'est pas la plus adaptée. Au début nous utilisions la combinaison plt.clf()+fig.canvas.draw()+plt.show() qui marchait sans message d'erreur. Mais plusieurs ordinateurs, dont ceux du lycee n'arrivaient pas à rafraichir,ils bloquaient car cette méthode est assez couteuse en ressource (mémoire vive). Ainsi la méthode actuelle semble la plus adaptée !

## Variables globales pouvant être modifiées par n'importe quelle fonction

posj1=10  #La courbure de la map étant composées de 400 points (générés par absc), on déplacera les joueurs sur cette courbe, il pourront prendre 400 emplacements différents sur la map (si la regle du jeu le permet ...)      
posj2=387 #On placera le joueur 1 à l'extrémité gauche et le joueur 2 à l'extremité droite au début de la partie

viej1=200  #Vie des joueurs
viej2=200

puissancej1=50      #Puissance de base des joueurs, dépend des projectiles utilisés
puissancej2=50

bonusj1=40      #Numéro du bonus gagné, initialisé à -1 ce qui signifie pas de bonus
bonusj2=40

deplacementj1=50    #Unités maximales de déplacement autorisées pour chaque joueur, peuvent être modifiées par un bonus
deplacementj2=50

impactj1=[[],[]]    #Variables qui prennent le dernier point d'impact des projectiles sur la map afin de les afficher sur la map statistique en fin de partie
impactj2=[[],[]]

statsvitesseanglej1=[[],[]]      #Variables prenant la vitesse des projectiles et leur angle pour afficher sur la page statistique
statsvitesseanglej2=[[],[]]

statbonus=[0,0]         #Variable qui compte les bonus attrapés par chaque joueur pour les stats en fin de partie
tirreussi=[0,0]         #Variable qui compte le nombre de tirs reussis par chaque joueur pour les stats en fin de partie

distanceparcourue=[0,0]     #Variable qui prend la distance parcourue par chaque joueur durant la partie pour les stats en fin partie


statsventprojectile=[0,0,[]]        #Variable qui prend le nombre de projectiles tirés ainsi que les vitesses prises par le vent pour les stats en fin partie 

statsproj=[[100,2.62e-05,30,16,70,105,0],[60, 1e-05,70,0,110,170,0],[300,1.8e-04,45,50,40,80,15]]        #[m,k,player dmg, map dmg,min speed,max speed,degats a distance]

choixproj1=0        #Variable qui prend le projectile choisi par chaque joueur
choixproj2=0

im=[] #Prend les ordonnées des points de la courbure de la map 
absc=np.linspace(0,6,400) # abscisse de la courbure de la map, formée de 400 points

beug=""
ia=""
touchéj1=False
touchéj2=False

start = time.time()     #Début du temps de jeu

chdir("C:\\Users\\adbla_000\\Documents\\Worms\\Info")
fichier=getcwd()



## Fonctions de création aléatoire d'un relief 

def caract(liste,n):        #on génère les variables aléatoires caracteristiques
    for i in range(0,n):
        liste.append(randint(0,50)/10)
    return liste

def fn(liste,x):            #on definit la courbe
    return (liste[0]*sin(liste[1]*x)+liste[2]*cos(liste[3]*x)+liste[4]*sin(liste[5]*x)+liste[6]*cos(liste[7]*x))
    


def ordo(absc,im,liste): 
              #on crée la liste des ordonnees
    for i in absc:
        im.append(fn(liste,i)*10)
    
    
def plats(im):                  #on place les bases aux extremités
    for i in range(0,len(im)):
        if i<40: im[i]=im[40]
        elif i>360: im[i]=im[360]

## Fonction de création de la map

def creationmap():

    global posj1, posj2,absc,im #Appel des variables globales
    
    liste=[]
    liste=caract(liste,100)       #Appel des fonctions de création de la courbure de la map...
    ordo(absc,im,liste)
    plats(im)
    
    absc=absc.tolist()
    
    for i in range(0,len(absc)):
        absc[i]=absc[i]*168              
     
     
## Fonctions affichant les informations graphiques  


def rafraichir(vent,positionbonus,x,i):       #A chaque fois que l'on appelle cette fonction, elle (ré)affiche les entités du jeu à l'écran, avec leurs nouvelles valeurs
    global im1,im2,im3,im6,im8,im1bis,im2bis
    
    plt.cla()       #On efface les derniers textes 
    texte(vent,positionbonus)  #Appel des fonctions qui affichent les textes sur la fenetre
    ATH()
    bonus()
    plt.ylim((min(im)-50,min(im)+600))  #Fixe les axes en fonction notamment de la valeur minimum  de la hauteur de la map (ordonnées im)
    plt.xlim((0,1000.0))
    
    if beug=="a":       #Le mode bug affiche des couleurs aléatoires 
        coul1=couleur()
        coul2=couleur()
        imj1=choice([im1,im1bis,im9])
        imj2=choice([im2,im2bis,im10])
    else:
        coul1='green'
        coul2='blue'
        imj1=im1
        imj2=im2
        
        
    plt.plot(absc[0:186],im[0:186],zorder=2, color=coul1)   #On affiche la courbure de la map ...en coloriant l'aire sous la courbe       
    plt.plot(absc[215:399],im[215:399],zorder=2, color=coul1)  #On laisse un espace au centre qui représentera une rivière, frontière infranchissable séparant les deux camps       
    plt.fill_between(absc[0:186],im[0:186],min(im)-50,zorder=2, color=coul1)  #... en coloriant l'aire sous la courbe    
    plt.fill_between(absc[185:216],min([im[185],im[216]])-10,min(im)-50,zorder=1, color=coul2)   #On colore en bleu la rivière
    plt.fill_between(absc[215:399],im[215:399],min(im)-50,zorder=2, color=coul1)
    
    plt.imshow(imj1, zorder=1, extent=[absc[posj1]-25, absc[posj1]+25, im[posj1], im[posj1]+50]) #On affiche les images des joueurs
    plt.imshow(imj2, zorder=1, extent=[absc[posj2]-25, absc[posj2]+25, im[posj2], im[posj2]+50])
    plt.imshow(im3, zorder=0, extent=[0,1000.0,min(im)-10,min(im)+600])     #Le fond d'écarn
    plt.imshow(im6, zorder=1, extent=[absc[positionbonus]-25, absc[positionbonus]+25, im[positionbonus], im[positionbonus]+50]) #Le bonus
    if x!=0 :       #Active la bombe atomique ou l'érosion si le bonus correspond
        if x==i:
            plt.imshow(im8, zorder=5, extent=[absc[x]-5,absc[x]+5,im[x],im[x]+10]) 
        else:
            plt.imshow(im7, zorder=5, extent=[absc[x]-50,absc[x]+50,i,i+100])  
        
      
    #Affichage des images : zorder c'est l'ordre de priorité des images (superposition, etc ) et extent c'est le taille des images selon le schéma [xbasgauche,xhautdroit,ybasgauche,yhautdroit]
    #On place les chars sur la courbure d'ou les parametre x et y en fonction de absc et im.
    #posj1 et posj2 varient des que l'on demande au joueurs d'avancer (voir fonction déplacement)
    #La troisieme image est le fond d'écran
    
    plt.pause(0.0001) #on affiche la fenetre 
    


def zoom(posj,joueur):  #Fait un zoom sur le joueur qui vient de subir des dégats, très semblable à la fonction raffraichir ...
    global tirreussi
    
    # plt.cla()
    # plt.title(joueur, style='italic',color='white', size=40)   #Nom du joueur touché
    # plt.ylim((im[posj],im[posj]+50))  #Fixe les axes en fonction notamment de la valeur minimum et maximum de la hauteur de la map (ordonnées im)
    # if posj==posj1:
    #     plt.xlim((absc[posj],absc[posj]+50))    #On fait un zoom sur la position d'un des deux joueurs
    # else:
    #     plt.xlim((absc[posj]-50,absc[posj]))
    # 
    # plt.plot(absc,im,zorder=2, color='green')            #On affiche la courbure de la map ...en coloriant l'aire sous la courbe       
    # plt.fill_between(absc,im,min(im)-10,zorder=2, color='green')  #... en coloriant l'aire sous la courbe       
    # 
    # plt.imshow(im3, zorder=0, extent=[0,1000.0,min(im)-10,max(im)+500])
    # plt.imshow(im1, zorder=0, extent=[absc[posj1], absc[posj1]+50, im[posj1], im[posj1]+50]) 
    # plt.imshow(im2, zorder=0, extent=[absc[posj2]-50, absc[posj2], im[posj2], im[posj2]+50])
    #
    if viejoueur(joueur)=="pas mort":           #Si  le tir ne tue pas le joueur on affiche juste une petit croix au-dessus
        if joueur=="joueur1":
            plt.imshow(im5, zorder=2, extent=[absc[posj1]-25, absc[posj1]+25, im[posj1], im[posj1]+50])
            tirreussi[1]+=1   #Un tir reussi de plus pour le joueur qui vient de toucher son adversaire
        else:
            plt.imshow(im5, zorder=2, extent=[absc[posj2]-25, absc[posj2]+25, im[posj2], im[posj2]+50])
            tirreussi[0]+=1 
    else : #Sinon on affiche le joueur avec une explosion dessus pour montrer qu'il est mort
        if joueur=="joueur1":
            plt.imshow(im4, zorder=2, extent=[absc[posj1]-25, absc[posj1]+25, im[posj1], im[posj1]+50]) 
            tirreussi[1]+=1 
        else:
            plt.imshow(im4, zorder=2, extent=[absc[posj2]-25, absc[posj2]+25, im[posj2], im[posj2]+50])
            tirreussi[0]+=1 
    
    plt.pause(1)    #La petite image reste 1 seconde au-dessus du joueur   


## Fonctions affichant les informations textuelles (fenêtre et console)

def ATH():      #On appelle les fonctions relatives à l'affichage de la vie et de la puissance
    vie()
    puissance()

    
def vie():      #Affichage de la barre de vie à l'écran
    global viej1,viej2
    
    if beug=="a":
        coul=couleur()
    else:
        coul='red'
        
    
    x1=np.linspace(0, viej1, viej1,endpoint=True)
    y1=[int((8/10)*(min(im)+600))]*int(viej1)
    plt.plot(x1,y1,color=coul, linewidth=5.0, linestyle="-")
    
    x2=np.linspace(1000-viej2, 1000, viej2,endpoint=True)
    y2=[int((8/10)*(min(im)+600))]*int(viej2)
    plt.plot(x2,y2,color=coul, linewidth=5.0, linestyle="-")
    
def puissance():#Affichage de la barre de puissance à l'écran
    global puissancej1,puissancej2
    
    if beug=="a":
        coul=couleur()
    else:
        coul='yellow'
    
    x1=np.linspace(0, puissancej1, puissancej1,endpoint=True)
    y1=[int((7/10)*(min(im)+600))]*int(puissancej1)
    plt.plot(x1,y1,color=coul, linewidth=5.0, linestyle="-")
    
    x2=np.linspace(1000-puissancej2, 1000, puissancej2,endpoint=True)
    y2=[int((7/10)*(min(im)+600))]*int(puissancej2)
    plt.plot(x2,y2,color=coul, linewidth=5.0, linestyle="-")


    
def texte(vent,positionbonus): #Affichage des différents textes en bas de l'écran
    global viej1,viej2,deplacementj1,deplacementj2
    
    if beug=="a":
        nom=choice(["L'Artilleur","Le Cannonier","Toto","NaN",])
    else:
        nom="L'Artilleur"    
    
    csfont = {'fontname':'fantasy'} #Police
    plt.title(nom, style='italic',color='white', size=40,**csfont )   #Le titre
    ax.text(0.0,0.0, '*** Joueur1 ***\n'+'->Vie : '+str(int(viej1))+'\n'+'->Position : '+str(int(absc[posj1]))+' m\n'+'->Deplacement max'+'\n'+'    autorisé : '+str(deplacementj1)+'\n',
            horizontalalignment='left',
            verticalalignment='top',
            transform=ax.transAxes) #Infos du joueur 1
    ax.text(0.80,0.0, '*** Joueur2 ***\n'+'->Vie : '+str(int(viej2))+'\n'+'->Position : '+str(int(absc[posj2]))+' m\n'+'->Deplacement max'+'\n'+'    autorisé : '+str(deplacementj2)+'\n',
            horizontalalignment='left',
            verticalalignment='top',
            transform=ax.transAxes) #Infos du joueur 2
    ax.text(0.40,0.0,'\nVent : '+str(int(-vent[0]))+' m/s\n" '+vent[1]+' "\n'+'\nPosition Bonus : '+str(int(absc[positionbonus]))+'\n', 
            horizontalalignment='left',
            verticalalignment='top',
            transform=ax.transAxes) #Infos pour les joueurs

            
            
          
def menu():     #Affichage du menu initial avec boucles de contrôle
    global beug,ia
    simsuc,ventoupasvent,bonus,plus="","","",""
    print("*************************************************\n")
    print("*******************Menu**************************\n")
    print("*************************************************\n")
    
    while ia!="a" and ia!="b" and ia!="c":
        print("\n\noxoxoxo Mode de jeu ? oxoxoxo\n")
        print("a-Joueur1 vs Joueur2!\n")
        print("b-Joueur1 vs Ia sans le mode shooting!\n")
        print("c-Joueur1 vs Ia avec le mode shooting!\n")
        
        print("Que choisissez-vous ?\n")
        ia=input("------>")
        
    while simsuc!="a" and simsuc!="b":
        print("\n\noxoxoxo Tour par tour ou Successif ? oxoxoxo\n")
        print("a-Tour par tour\n")
        print("b-Simultané\n")
        print("Que choisissez-vous ?\n")
        simsuc=input("------>")
        
    while ventoupasvent!="a" and ventoupasvent!="b" and ventoupasvent != "c":
        print("\n\noxoxoxo Vent ? oxoxoxo\n")
        print("a-Différent à chaque tour\n")
        print("b-Même à chaque tour\n")
        print("c-Pas de vent\n")
        print("Que choisissez-vous ?\n")
        ventoupasvent=input("------>")
        
    while bonus!="a" and bonus!="b" and bonus != "c":
        print("\n\noxoxoxo Bonus ? oxoxoxo\n")
        print("a-Oui\n")
        print("b-Non\n")
        print("Quel  choisissez-vous ?\n")
        bonus=input("------>")
    
    
        
    while beug!="a" and beug!="b":
        print("\n\noxoxoxo D'autres envies ? oxoxoxo\n")
        print("a-Le mode beuggé s'il vous plait !\n")
        print("b-Non\n")
        
        print("Que choisissez-vous ?\n")
        beug=input("------>")
        
    return simsuc,ventoupasvent,bonus
    
    
## Fonctions réservées au bonus

def bonus():        #Place le bonus aléatoirement sur la map
    
    # positionbonus1=int(uniform(30,60.0)) #Place près du camp de départ pour faciliter les tests
    # positionbonus2=int(uniform(330.0,370.0))
    positionbonus1=int(uniform(30,170.0)) #Place n'importe ou (sauf eau)
    positionbonus2=int(uniform(230.0,370.0))
    positionbonus=choice([positionbonus1,positionbonus2]) #Choisi le côté ou l'on place le bonus (camp j1 ou campj2)
    
    return positionbonus

def machineabonus(bonusrecu,j,vent,positionbonus):      #Un fois le bonus attrapé, on appelle cette fonction qui gère certains bonus et le texte de description contenu dans une base de donnée
    global bonusj1,bonusj2
    
    if j=="joueur1":        #On augmente le compteur de bonus pour les stats du joueur concerné
        statbonus[0]+=1
    else:
        statbonus[1]+=1
    
    fichierDonnees ="C:/Users/adbla_000/Documents/Worms/Info/Bdd Artilleur.db" #On va rechercher l'emplacement de la base de donnée
    conn =sqlite3.connect(fichierDonnees)
    cur =conn.cursor()      #On crée le curseur pour se déplacer dans la bdd
    # cur.execute("SELECT * FROM bonus")
    
    id=str(bonusrecu)       #On transforme le nombre du bonus obtenu en chaine de caractère pour afficher le texte qui lui correspond (on cherche l'enregistrement ayant l'id correspondant en fait)
    cur.execute("SELECT Nom,Description FROM bonus Where Id =="+id+";")
    
    for l in cur:   #On affiche le seul texte correpondant au bonus attrapé
        print("\nVotre bonus "+j+" est :",l[0])
        print("\nDescription : ",l[1])
    
    if bonusj1==1 or bonusj2==1 or bonusj1==2 or bonusj2==2: #En fonction du bonus attrapé, certaines actions vont se déclancher pour le tour de jeu
        # print(bonusj1,bonusj1)
        levelupdown()
    if bonusj1==3 or bonusj2==3 or bonusj1==4 or bonusj2==4:
        speedupdown()
    if bonusj1==5 or bonusj2==5:
        twist()
    if bonusj1==6 or bonusj2==6 or bonusj1==7 or bonusj2==7:
        bombeatomiquepluie(vent,positionbonus)
    
    cur.close() #On ferme le curseur et la bdd
    conn.close()
     
    
def couleur():      #Fonction appelée pour changer la couleur de tout et n'importe quoi de manière aléatoire
    couleur="#"
    for i in range (0,6,1):
        couleur=couleur+choice(["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"])
    return couleur
    
def marqueur():
    marq=choice([".",",","o","v","^","<",">","1","2","3","4","8","s","p","*","h","H","+","x","D","d","|","_"])
    return marq

def point2():       #Fonction qui renvoit un nombre au hasard entre 0 et 100
    taillepoint=uniform(0.0,50.0)
    return taillepoint
    
def levelupdown():      #Fonction qui modifie la vie du joueur 
    global viej1,viej2
    # print(bonusj1,bonusj1,type(bonusj1))
    
    if bonusj1==1 or bonusj1==2:
        if bonusj1==1:
            viej1*=2
        else:
            viej1/=2
    if bonusj2==1 or bonusj2==2:
        if bonusj2==1:
            viej2*=2
        else:
            viej2/=2
            
def degatupdown(): #Fonction qui modifie les dégats infligés par le joueur
    global puissancej1,puissancej2
    
    if bonusj1==10 or bonusj1==11:
        if bonusj1==10:
            puissancej1*=2
        else:
            puissancej1/=2
    if bonusj2==10 or bonusj2==11:
        if bonusj2==10:
            puissancej2*=2
        else:
            puissancej2/=2
            
def speedupdown():      #Fonction qui modifie le nombre de déplacement autorisé
    global deplacementj1,deplacementj2
    
    if bonusj1==3 or bonusj1==4:
        if bonusj1==3:
            deplacementj1*=2
        else:
            deplacementj1=int(deplacementj1/2)
    if bonusj2==3 or bonusj2==4:
        if bonusj2==3:
            deplacementj2*=2
        else:
            deplacementj2=int(deplacementj2/2)
         
def twist():        #Inverse la vie et les unités de déplacement des deux joueurs
    global viej1,viej2,deplacementj1,deplacementj2
    
    viej1,viej2=viej2,viej1
    deplacementj1,deplacementj2=deplacementj2,deplacementj1
    


def tricheur(x,y,vent,positionbonus,joueur):           #Permet au houeur de voir la trajectoire du projectile et de rejoueur si il le souhaite
    global ia
    
    changer=""
    choixiatricheur=True
    plt.plot(x,y, 'x', ms=7,color = 'red')      #On affiche la trajectoire du projectile
    plt.pause(0.01)
    
    if ia!="a" and joueur=="joueur2":
        choixiatricheur=analyseia(positionbonus,vent,False)[4]
        return choixiatricheur
    else:
        while 1:        #On demande au joueur si elle lui convient
            print("\n\noxoxoxo Changer de paramètres de tir ? oxoxoxo\n")
            print("1-Oui\n")
            print("2-Non\n")
            print("Quel  choisissez-vous ?\n")
            changer=input("------>")
            if changer.isdigit():
                changer=int(changer)
                if changer!=1 and changer!=2:
                    print("invalide")
                elif changer==1:
                    return True     #Si elle ne lui convient pas, la fonction renvoit True pour que le joueur puisse rejouer
                elif changer==2:
                    return False
            else:
                print("entrez une valeur numérique svp")
        

def modenfer(vent,positionbonus,joueur):
    global ia
    choixiaenfer=True
    
    if ia!="a" and joueur=="joueur2":
        choixiaenfer=analyseia(positionbonus,vent,False)[5]
        return choixiaenfer

    else:
        while 1:        #On demande au joueur si elle lui convient
            print("\n\noxoxoxo Activer le mode enfer (-90 pv pour vous si utilisation !) ? oxoxoxo\n")
            print("1-Oui\n")
            print("2-Non\n")
            print("Quel  choisissez-vous ?\n")
            enfer=input("------>")
            if enfer.isdigit():
                enfer=int(enfer)
                if enfer!=1 and enfer!=2:
                    print("invalide")
                elif enfer==1:
                    return True     #Si elle ne lui convient pas, la fonction renvoit True pour que le joueur puisse rejouer
                elif enfer==2:
                    return False
            else:
                print("entrez une valeur numérique svp")
    

def affichagebombepluie(x,vent,positionbonus):      #Animation de la tombée de la bombe atomique
    i=int(max(im)+500)
    
    while i>im[x]-100:
        rafraichir(vent,positionbonus,x,i)
        i-=200

def bombeatomiquepluie(vent,positionbonus):         #Gère les bonus de la bombe atomique et de la pluis acide
    global im,absc,viej1,viej2
    nbbombes=""
    
    if bonusj1==6 or bonusj2==6: #Si on a attrapé le bonus 11 qui est celui de la bombe atomique
    
        if bonusj2==6 and ia!="a":
            nbbombes=randint(0,5)
        else:
            while nbbombes.isdigit()==False:
                print("\n\noxoxoxo Nombre de bombes ? oxoxoxo\n")
                print("Que choisissez-vous (Si vous demandez trop de bombes, cela risque de finir sur une égalité ;) ?\n")
                nbbombes=input("------>")
            nbbombes=int(nbbombes)
            
        for u in range (0,nbbombes):       #On va balancer deux bombes
            x=int(uniform(1.0,399.0))  #Sa position est aléatoire
            affichagebombepluie(x,vent,positionbonus)  #On anime sa descente
            if posj1-25<x<posj1+25:
                if viej1-50>0:
                    viej1-=50
                else:
                    viej1=0
            if posj2-25<x<posj2+25:
                if viej2-50>0:
                    viej2-=50
                else:
                    viej2=0
        
            pilouface=1
            if beug=="a":
                pilouface=randint(1,2)      #Si pileouface==1 on fait des buttes, sinon on fait des creux
                
            if pilouface==2:
                im[x]+=144      #On détruit un petit peu la map sur 60 points de largeur avec une profondeur de 144 points pour le centre de l'explosion :) 
            else:
                im[x]-=144 
                
            for i in range(1,60):
                if x-i>=0:
                    if pilouface==2:
                        im[x-i]+=144-(i/5)**2
                    else:
                        im[x-i]-=144-(i/5)**2
                if x+i<=399:
                    if pilouface==2:
                        im[x+i]+=144-(i/5)**2
                    else:
                        im[x+i]-=144-(i/5)**2
                        
    if bonusj1==7 or bonusj2==7:    #Si on a attrapé le bonus 13 qui est celui de la pluie acide
        for u in range (0,30): #On va créer 100 petits impacts de pluie sur la map
            x=int(uniform(1.0,399.0))   #Leur position est aléatoire
            rafraichir(vent,positionbonus,x,x)#On anime les petites gouttes de pluie
            if posj1-25<x<posj1+25:
                if viej1-2>0:
                    viej1-=2
                else:
                    viej1=0
            if posj2-25<x<posj2+25:
                if viej2-2>0:
                    viej2-=2
                else:
                    viej2=0
            pilouface=1
            if beug=="a":
                pilouface=randint(1,2)
                
            if pilouface==2:
                im[x]+=16
            else:
                im[x]-=16

            for i in range(1,7):
                if x-i>=0 :
                    if pilouface==2:
                        im[x-i]+=16-(i/1.5)**2
                    else:
                        im[x-i]-=16-(i/1.5)**2
                if x+i<=399:
                    if pilouface==2:
                        im[x+i]+=16-(i/1.5)**2
                    else:
                        im[x+i]-=16-(i/1.5)**2
                        

    rafraichir(vent,positionbonus,0,0)  #On raffraichi le tout ca fait pas de mal      
    fig.canvas.draw()
    
    
def multitir(vitesse,angle,posj,joueur,posjadv,joueuradv,positionbonus,vent,typ):       #Fonction qui démultiplie le tir
    
    tableaumultitir=[]
    if typ=="enfer":
        dev=20
    else:
        dev=0
    
    for i in range(0,2):# On appelle les fonctions de création de trajectoire avec les mêmes parametres que le tir central mais en changeant l'angle
        tableaumultitir.append(creationdetrajectoire(absc[posj],im[posj]+50,joueur,vent,posjadv,joueuradv,angle+(i+1)*10,vitesse+i*dev,positionbonus))
        tableaumultitir.append(creationdetrajectoire(absc[posj],im[posj]+50,joueur,vent,posjadv,joueuradv,angle-(i+1)*10,vitesse+i*dev,positionbonus))
 
    return tableaumultitir
    

## Fonction corps du programme     

def Jeu(choix1,vent,positionbonus):        #Fonction qui s'occupe de tracer les courbes des projectiles pour les deux joueurs
    global posj1,posj2,absc,im,bonusj1,bonusj2,viej1,viej2
    
    tableaumultitirj1=[]    #Initialisation des tableaux prenant les coordonnées des tirs multiples, la plupart du temps, ils restent vides
    tableaumultitirj2=[]
    
    if choix1 == "a":       #Si on joue au tour par tour
        
        deplacement("joueur1",vent,positionbonus)     #Appel de la fonction deplacement joueur1 
        rafraichir(vent,positionbonus,0,0)  
        tabcoordonées=creationdetrajectoire(absc[posj1],im[posj1]+50,"joueur1",vent,posj2,"joueur2",0,0,positionbonus) #On obtient les points de la trajectoire
        x=tabcoordonées[0]       #On recupère les coordonnées des points de la trajectoire...
        y=tabcoordonées[1]
    
        if bonusj1==8:  #Si le bonus tricheur est activé ...
            rejouer=tricheur(x,y,vent,positionbonus,"joueur1")
            if rejouer==True:# ... et que le joueur décide de rejouer ...
                statsventprojectile[0]-=1  #(Le dernier projectile est annulé dans les stats)
                tabcoordonées=creationdetrajectoire(absc[posj1],im[posj1]+50,"joueur1",vent,posj2,"joueur2",0,0,positionbonus) #...il rejoue
                x=tabcoordonées[0]       
                y=tabcoordonées[1]
                rafraichir(vent,positionbonus,0,0)
                
        if beug=="a":
            enfer=modenfer(vent,positionbonus,"joueur1")
            if enfer==True:
                tableaumultitirj1=multitir(tabcoordonées[2],tabcoordonées[3],posj1,"joueur1",posj2,"joueur2",positionbonus,vent,"enfer")
                if viej1-90>=0:
                    viej1-=90
                else:
                    viej1=0
                rafraichir(vent,positionbonus,0,0)
            
        
        if bonusj1==9:  #Si le bonus multitir est activé, en plus du tir central viendront s'ajouter des tirs supplémentaires
            tableaumultitirj1=multitir(tabcoordonées[2],tabcoordonées[3],posj1,"joueur1",posj2,"joueur2",positionbonus,vent,"bonus")
                
        mouvementprojectile(x, y,[],[],vent,positionbonus,tableaumultitirj1,[])     #On trace le mouvement des projectiles 
         
          
        deplacement("joueur2",vent,positionbonus)     #Appel de la fonction deplacement joueur1, mêmes choses que pour le joueur 1
        rafraichir(vent,positionbonus,0,0)  
        tabcoordonées=creationdetrajectoire(absc[posj2],im[posj2]+50,"joueur2",vent,posj1,"joueur1",0,0,positionbonus) 
        x=tabcoordonées[0]       #On recupère les coordonnées des points des deux trajectoires...
        y=tabcoordonées[1]
        
        if bonusj2==8:
            rejouer=tricheur(x,y,vent,positionbonus,"joueur2")
            if rejouer==True:
                statsventprojectile[1]-=1 
                tabcoordonées=creationdetrajectoire(absc[posj2],im[posj2]+50,"joueur2",vent,posj1,"joueur1",0,0,positionbonus) 
                x=tabcoordonées[0]
                y=tabcoordonées[1]
                rafraichir(vent,positionbonus,0,0)
        
        if beug=="a":
            enfer=modenfer(vent,positionbonus,"joueur2")
            if enfer==True:
                tableaumultitirj2=multitir(tabcoordonées[2],tabcoordonées[3],posj2,"joueur2",posj1,"joueur1",positionbonus,vent,"enfer")
                if viej2-90>=0:
                    viej2-=90
                else:
                    viej2=0
                rafraichir(vent,positionbonus,0,0)
                
        if bonusj2==9:
            tableaumultitirj2=multitir(tabcoordonées[2],tabcoordonées[3],posj2,"joueur2",posj1,"joueur1",positionbonus,vent,"bonus")
                
        mouvementprojectile([],[],x,y,vent,positionbonus,[],tableaumultitirj2)     #On trace le mouvement des projectiles

    else :      #Si on joue en simultané, les fonctions appelée sont les mêes que plus haut mais dans un ordre différent
        deplacement("joueur1",vent,positionbonus)
        deplacement("joueur2",vent,positionbonus) #Appel de la fonction  deplacement joueur2
    #Les paramètres "joueur1" et "joueur2" sont utiliser dans une question posée a l'utilisateur et  permettent d'orienter le programme 
        
        rafraichir(vent,positionbonus,0,0)
        tabcoordonéesj1=creationdetrajectoire(absc[posj1],im[posj1]+50,"joueur1",vent,posj2,"joueur2",0,0,positionbonus) #Appel de la fonction de creation de trajectoire 
        tabcoordonéesj2=creationdetrajectoire(absc[posj2],im[posj2]+50,"joueur2",vent,posj1,"joueur1",0,0,positionbonus) 
    #En paramètre, on donne la position des joueurs sur la courbure, "joueur1" et "joueur2" sont utiliser dans une question posée a l'utilisateur et  permettent d'orienter le programme

        x1=tabcoordonéesj1[0]       #On recupère les coordonnées des points des deux trajectoires...
        y1=tabcoordonéesj1[1]       
        x2=tabcoordonéesj2[0]
        y2=tabcoordonéesj2[1]
        
                
        if bonusj1==8:
            rejouer=tricheur(x1,y1,vent,positionbonus,"joueur1")
            if rejouer==True:
                statsventprojectile[0]-=1
                tabcoordonéesj1=creationdetrajectoire(absc[posj1],im[posj1]+50,"joueur1",vent,posj2,"joueur2",0,0,positionbonus)
                x1=tabcoordonéesj1[0]       
                y1=tabcoordonéesj1[1] 
                rafraichir(vent,positionbonus,0,0)
                
        if bonusj2==8:
            rejouer=tricheur(x2,y2,vent,positionbonus,"joueur2")
            if rejouer==True:
                statsventprojectile[1]-=1
                tabcoordonéesj2=creationdetrajectoire(absc[posj2],im[posj2]+50,"joueur2",vent,posj1,"joueur1",0,0,positionbonus) 
                x2=tabcoordonéesj2[0]
                y2=tabcoordonéesj2[1]
                rafraichir(vent,positionbonus,0,0)
        
        if bonusj1==9:
            tableaumultitirj1=multitir(tabcoordonéesj1[2],tabcoordonéesj1[3],posj1,"joueur1",posj2,"joueur2",positionbonus,vent,"bonus")
        if bonusj2==9:
            tableaumultitirj2=multitir(tabcoordonéesj2[2],tabcoordonéesj2[3],posj2,"joueur2",posj1,"joueur1",positionbonus,vent,"bonus")
            
        if beug=="a":
            enfer=modenfer(vent,positionbonus,"joueur1")
            if enfer==True:
                tableaumultitirj1=multitir(tabcoordonéesj1[2],tabcoordonéesj1[3],posj1,"joueur1",posj2,"joueur2",positionbonus,vent,"enfer")
                if viej1-90>0:
                    viej1-=90
                else:
                    viej1=0
                rafraichir(vent,positionbonus,0,0)
                
        if beug=="a":
            enfer=modenfer(vent,positionbonus,"joueur2")
            if enfer==True:
                tableaumultitirj2=multitir(tabcoordonéesj2[2],tabcoordonéesj2[3],posj2,"joueur2",posj1,"joueur1",positionbonus,vent,"enfer")
                if viej2-90>=0:
                    viej2-=90
                else:
                    viej2=0
                rafraichir(vent,positionbonus,0,0)
            
        rafraichir(vent,positionbonus,0,0)
        mouvementprojectile(x1, y1, x2, y2,vent,positionbonus,tableaumultitirj1,tableaumultitirj2)     #On trace le mouvement des projectiles
    
    

    if bonusj1!=40 or bonusj2!=40: #Si le bonus a été attrapé
        bonusj1=-1      
        bonusj2=-1

    rafraichir(vent,positionbonus,0,0)
 
    
## Fonctions qui gérent le projectile dans son environnement           
            
def testpointvalide(x,y,posj,joueurtouche): #On vérifie si le point est bien au dessus de la map
    
    invaliditepoint=False
    
    point=int((x/1000)*400)#Opération étrange mais nécessaire : la coordonnée x du point (entre 0 et 1000) et ramenée sur l'échelle(0,400) pour pouvoir ensuite l'utilisée comme un compteur. Exemple si x1[i] =500, c'est à dire que le point est au milieu de la map, alors (x1[i] /1000)*400 devient 200 ce qui correspond a la case du tableau contenant la coordonnée x du milieu de la courbure de la map (absc[200])

    if point>=0 and point<400:#point1 doit etre compris entre 0 et 399 pour etre utilisé comme compteur( ou indice) de absc et im
        if y<im[point]: #Si le projectile touche la courbure ...
            invaliditepoint=True  # ... alors on stoppe le tracage de la courbe
    return invaliditepoint           
    
    
def affichepoints(x,y,i,bonus,line):    #On affiche les points sur la map lors du tir
    bool=False
    
    line.set_data(x[i], y[i])#On affiche un nouveau point et efface le précédent

    if beug=="a": #Si le bonus changement de taille est activé le projectile change constamment de 
        line.set_ms(point2())
        line.set_marker(marqueur())
        line.set_color(couleur())
            
def toucherjoueur(x,y,posj,joueur):        #Fonction qui renseigne si le projectile est sur le joueur ou non

    a=absc[posj]#position du joueur selon l'abscisse
    b=im[posj]
    # print("a",a,"b",b)
    # print("x",x,"y",y)
    if joueur=="joueur1":
        if a-25<=x<=a+25 and b<=y<=b+50:       #Zone occupée par le joueur 1
            return True 
        else :
            return False
    else :
        if a-25<=x<=a+25 and b<=y<=b+50:       #Zone occupée par le joueur 2
            return True
        else:
            return False
   
def degatsdezone(x,y,posj,joueur):
    a=absc[posj]#position du joueur selon l'abscisse
    b=im[posj]
    # print("a",a,"b",b)
    # print("x",x,"y",y)
    if joueur=="joueur1":
        if a-75<=x<a-25 or a+25<x<=a+75:       #Zone occupée par le joueur 1
            return True 
        else :
            return False
    else :
        if a-75<=x<a-25 or a+25<x<=a+75:       #Zone occupée par le joueur 2
            return True
        else:
            return False
    


def cratere(x,vent,positionbonus,trou):     #Trace un cratère sur l'endroit touché par le projectile
    global im,absc
    
    
    x=int((x/1000)*400)
    pilouface=1
    if beug=="a":
        pilouface=randint(1,2)
    if 0<=x<=399:
        if pilouface==2:
            im[x]+=trou
        else:
            im[x]-=trou
    for i in range(1,2*int(1.5*sqrt(trou))):
        if x-i>=0 and x+i<=399:
            if pilouface==2:
                im[x-i]+=trou-((i/1.5)**2)/4
                im[x+i]+=trou-((i/1.5)**2)/4
            else:
                im[x-i]-=trou-((i/1.5)**2)/4
                im[x+i]-=trou-((i/1.5)**2)/4
    fig.canvas.draw()



def mouvementprojectile(x1, y1, x2, y2,vent,positionbonus,tableaumultitirj1,tableaumultitirj2):  #Fonction qui s'occupe de l'animation du projectile
    global choixproj1,choixproj2,statsproj,viej1,viej2,impactj1,impactj2,touchéj1,touchéj2

    line1, = ax.plot([], [], 'bo', ms=7,zorder=4,color = "red") #On déclare des axes sur lesquels on tracent les trajectoires
    line11, = ax.plot([], [], 'bo', ms=7,zorder=4,color = "red") 
    line111, = ax.plot([], [], 'bo', ms=7,zorder=4,color = "red") 
    line1111, = ax.plot([], [], 'bo', ms=7,zorder=4,color = "red") 
    line11111, = ax.plot([], [], 'bo', ms=7,zorder=4,color = "red") 
    line2, = ax.plot([], [], 'bo', ms=7,zorder=4,color = "red") 
    line22, = ax.plot([], [], 'bo', ms=7,zorder=4,color = "red") 
    line222, = ax.plot([], [], 'bo', ms=7,zorder=4,color = "red") 
    line2222, = ax.plot([], [], 'bo', ms=7,zorder=4,color = "red") 
    line22222, = ax.plot([], [], 'bo', ms=7,zorder=4,color = "red") 
    
    i=0     #Deux variables inutiles ...
    bool=False
    
    xi1=True
    xi2=True
    
    touchéj1=False
    touchéj2=False
    
    if x1==[]: xi1=False
    if x2==[]: xi2=False
    
    
    xa1,ya1,xb1,yb1,xc1,yc1,xd1,yd1,xa2,ya2,xb2,yb2,xc2,yc2,xd2,yd2=[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[] #Tableaux de points pour les trajectoires centrales et le mutlitir
    if len(tableaumultitirj1)>0:        #Si on possède le bonus multitir, on recupère les coordonnées des points supplémaentaires
        xa1,ya1,xb1,yb1,xc1,yc1,xd1,yd1=tableaumultitirj1[0][0],tableaumultitirj1[0][1],tableaumultitirj1[1][0],tableaumultitirj1[1][1],tableaumultitirj1[2][0],tableaumultitirj1[2][1],tableaumultitirj1[3][0],tableaumultitirj1[3][1]
    if len(tableaumultitirj2)>0:
        xa2,ya2,xb2,yb2,xc2,yc2,xd2,yd2=tableaumultitirj2[0][0],tableaumultitirj2[0][1],tableaumultitirj2[1][0],tableaumultitirj2[1][1],tableaumultitirj2[2][0],tableaumultitirj2[2][1],tableaumultitirj2[3][0],tableaumultitirj2[3][1]
        
    
    # print(x1,impactj1,impactj2)
    while(len(x1)>i or len(x2)>i or len(xa1)>i or len(xb1)>i or len(xc1)>i or len(xd1)>i or len(xa2)>i or len(xb2)>i or len(xc2)>i or len(xd2)>i  ):#Tant que tous les points valables (on s'arrète aux points qui sortent de la map et ceux qui rentrent dans les obstacles) n'ont pas été affiché
    
        if len(x1)>i: #Si il reste encore des points à afficher
            affichepoints(x1,y1,i,bonusj1,line1,)
            if toucherjoueur(x1[i], y1[i], posj2, "joueur2")==True: #Si le joueur est touché alors on stoppe la course du projectile
                zoom(posj2,"joueur2")       #On appelle la fonction qui affiche le joueur touché et lui retire de la vie (On peux activer un zoom si on le souhaite dans cette fonction manuellement)
                x1=[]       #Le joueur étant touché, le projectile n'existe plus
                touchéj1=True
                
        if 0<len(x1)<=i+4 and 0<x1[-1]<1000: #Si le projectile tombe dans la zone de jeu
            
            cratere(x1[-1],vent,positionbonus,statsproj[choixproj1][3]) #On afiche un cratère la ou il est tombé
            x1=[]  #Le projectile n'existe plus
            
        if len(xa1)>i:#Même chose que plus haut pour les autres if
            affichepoints(xa1,ya1,i,bonusj1,line11,)
            if toucherjoueur(xa1[i], ya1[i], posj2, "joueur2")==True: 
                zoom(posj2,"joueur2")
                xa1=[]
        if 0<len(xa1)<=i+4 and 0<xa1[-1]<1000:
            cratere(xa1[-1],vent,positionbonus,statsproj[choixproj1][3])
            xa1=[]
            
        if len(xb1)>i:
            affichepoints(xb1,yb1,i,bonusj1,line111,)
            if toucherjoueur(xb1[i], yb1[i], posj2, "joueur2")==True: 
                zoom(posj2,"joueur2")
                xb1=[]
        if 0<len(xb1)<=i+4 and 0<xb1[-1]<1000:
            cratere(xb1[-1],vent,positionbonus,statsproj[choixproj1][3])
            xb1=[]        
                
        if len(xc1)>i:
            affichepoints(xc1,yc1,i,bonusj1,line1111,)
            if toucherjoueur(xc1[i], yc1[i], posj2, "joueur2")==True:
                zoom(posj2,"joueur2")
                xc1=[]
        if 0<len(xc1)<=i+4 and 0<xc1[-1]<1000:
            cratere(xc1[-1],vent,positionbonus,statsproj[choixproj1][3])
            xc1=[]          
                
        if len(xd1)>i:
            affichepoints(xd1,yd1,i,bonusj1,line11111,)
            if toucherjoueur(xd1[i], yd1[i], posj2, "joueur2")==True:
                zoom(posj2,"joueur2")
                xd1=[]
        if 0<len(xd1)<=i+4 and 0<xd1[-1]<1000:
            cratere(xd1[-1],vent,positionbonus,statsproj[choixproj1][3])
            xd1=[]   
    
        
        
        if len(x2)>i:
            affichepoints(x2,y2,i,bonusj2,line2,)
            if toucherjoueur(x2[i], y2[i], posj1, "joueur1")==True:
                zoom(posj1,"joueur1")
                x2=[]
                touchéj2=True
            
            if 0<len(x2)<=i+4 and 0<x2[-1]<1000:
                cratere(x2[-1],vent,positionbonus,statsproj[choixproj2][3])
                x2=[]      
                
         
        if len(xa2)>i:
            affichepoints(xa2,ya2,i,bonusj2,line22,)
            if toucherjoueur(xa2[i], ya2[i], posj1, "joueur1")==True:
                zoom(posj1,"joueur1")
                xa2=[]
            if 0<len(xa2)<=i+4 and 0<xa2[-1]<1000:
                cratere(xa2[-1],vent,positionbonus,statsproj[choixproj2][3])
                xa2=[]      
                
        if len(xb2)>i:
            affichepoints(xb2,yb2,i,bonusj2,line222,)
            if toucherjoueur(xb2[i], yb2[i], posj1, "joueur1")==True: 
                zoom(posj1,"joueur1")
                xb2=[]
            if 0<len(xb2)<=i+4 and 0<xb2[-1]<1000:
                cratere(xb2[-1],vent,positionbonus,statsproj[choixproj2][3])
                xb2=[]       
                
        if len(xc2)>i:
            affichepoints(xc2,yc2,i,bonusj2,line2222,)
            if toucherjoueur(xc2[i], yc2[i], posj1, "joueur1")==True: 
                zoom(posj1,"joueur1")
                xc2=[]
            if 0<len(xc2)<=i+4 and 0<xc2[-1]<1000:
                cratere(xc2[-1],vent,positionbonus,statsproj[choixproj2][3])
                xc2=[]       
                
        if len(xd2)>i:
            affichepoints(xd2,yd2,i,bonusj2,line22222,)
            if toucherjoueur(xd2[i], yd2[i], posj1, "joueur1")==True: 
                zoom(posj1,"joueur1")
                xd2=[]
            if 0<len(xd2)<=i+4 and 0<xd2[-1]<1000:
                cratere(xd2[-1],vent,positionbonus,statsproj[choixproj2][3])
                xd2=[]      
                

        if len(x1)>i and len(x2)>i: #Si les deux projectiles sont encore en mouvement ... 
            if x2[i]-15<=x1[i]<=x2[i]+15 and y2[i]-15<=y1[i]<=y2[i]+15:# ...Et qu'il entre en collision
                x2=[]# On stoppe leur course
                x1=[]
        # On peux rajouter 5  comparaisons pour le cas où un joueur a un multitir et les deux joueurs jouent en simultané
        fig.canvas.draw() #On trace le tout
    
        
      
        i+=3   #On affiche pas tout les points de la courbe(trop nombreux) mais 1 sur 3 pour que la vitesse soit réaliste (la vitesse peut varier en fonction de la puissance de l'ordinateur aussi ...)
    
        plt.pause(0.0001)
    if x1==[] and xi1==True and touchéj1==False :
        if degatsdezone(impactj1[0][-1],impactj1[1][-1],posj2,"joueur2")==True:
            if viej2-statsproj[choixproj1][6]>0:
                viej2-=statsproj[choixproj1][6] 
            else :
                viej2=0
            
    if x2==[] and xi2==True and touchéj2==False:        
        if degatsdezone(impactj2[0][-1],impactj2[1][-1],posj1,"joueur1")==True:
            if viej1-statsproj[choixproj2][6]>0:
                viej1-=statsproj[choixproj2][6]
            else:
                viej1=0
          
    rafraichir(vent,positionbonus,0,0)
    

##  Fonctions qui gérent la vie du joueur après s'être fait touché   

def viejoueur(joueur):  #Gère la vie du joueur nottament lorsque il est touché
    
    global viej1,viej2,puissancej1,puissancej2,beug
    
    pilouface=1
    if beug=="a":
        pilouface=randint(1,2)
    
    if joueur=="joueur1" :
        if viej1-puissancej2>=0: 
            if pilouface==1:
                viej1-=puissancej2   #On retire comme vie à j1 l'équivalent de la puissance de tir de j2
                vie=viej1
            else:
                viej1+=puissancej2   #On retire comme vie à j1 l'équivalent de la puissance de tir de j2
                vie=viej1
        else:
            viej1=0
            vie=viej1
        
    if joueur=="joueur2": 
        if viej2-puissancej1>=0: 
            if pilouface==1:
                viej2-=puissancej1
                vie=viej2
            else:
                viej2+=puissancej1
                vie=viej2
        else:
            viej2=0
            vie=viej2
        
        
    
    if vie>0:     #Renvoie des infos sur l'état du joueur
        return "pas mort" 
    else:
        return "mort"
        
        
## Petites fonctions mathématiques :-) 
    
def convertionangle(angle):
    angle=(angle/360)*2*pi    
    return angle
 
def moyenne(tab):
    moyenne=0
    l=len(tab)
    for i in tab:
        moyenne+=(i/l)
    return moyenne 
    
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False    

def isint(value):
  try:
    int(value)
    return True
  except ValueError:
    return False 


## Les fonctions de l'IA
def testrajectoire(m,vitesse,anglev,vitessevent):   #Utilisé par le mode shooting de l'ia
    
    pas=0.1
    g=9.81
    k=2.62e-05 #(1/2)*masse volumique de l'air(=1,29 kg/m3)*S la surface de contact offerte à la circulation d’air(0.25m carré)* coefficient de traînée Cx (donné dans table = drag coefficient
       #masse du projectile
    anglev=(anglev*2*pi)/360
    vx = vitesse*cos(anglev)
    x=absc[posj2]
    vy = vitesse*sin(anglev) 
    y=im[posj2]
    
    tabvx=[vx]
    tabx=[x] 
    tabvy=[vy]
    taby=[y]
    
    i=0
    testpoint=False
    while testpoint==False and min(im)<=y: 
        vxold=vx
        xold=x
        vyold=vy
        yold=y
        vx=vxold+pas*(-(k/m)*((sqrt((vyold)**2+(vxold+vitessevent)**2))*(vxold+vitessevent)))
        vy=vyold+pas*(-g-(k/m)*((sqrt((vyold)**2+(vxold+vitessevent)**2))*(vyold)))
        x=xold-vxold*pas     
        y=yold+vyold*pas 
        
        tabvx.append(vx)
        tabx.append(x) 
        tabvy.append(vy)
        taby.append(y)
        i+=1
        testpoint=testpointvalide(x,y,posj1,"joueur1") 
            
    return tabx,taby
    
# def der(theta,fit):#Ytilisé pors des test avec newton mais nous avons préféré la regression polynomiale
#     
#     return 5*fit[0]*theta**4+4*fit[1]*theta**3+3*fit[2]*theta**2+ 2*fit[3]*theta**1+fit[4]
   
def shooting(m,vitesse,anglev,vitessevent):  #Cherche l'angle optimal pour atteindre sa cible
    w=[]
    thet=[]
    for i in np.arange(0,90,0.05): # On fait defiler les angles de 0 a 90 degre
        tabcoordonées1=testrajectoire(m,vitesse,i,vitessevent)    
        # tabcoordonées2=creationdetrajectoire2(100.0,100.0,i,20.0) 
        x=tabcoordonées1[0][-1]
        w.append(x-(absc[posj1]))# On regarde la difference de la position du joueur1 à celle du projectile pour un angle donné 
        thet.append(i)
    # print(w)
    
    fit = np.polyfit(thet,w, 10)#Regression polynomiale prenant la différence décrite plus haut, le zero correspond à l'angle optimal
    # poly = np.poly1d(fit) #Coefficient du polynome
    # Plus utilisé
    # plt.plot(thet,poly(thet),"green")
    # plt.plot(thet,w,"blue")
    # plt.show()
  
    # theta=90
    # y=theta-(poly(theta)/der(theta,fit))
    # 
    # while (theta-y)>0.01:
    #     theta=y
    #     y=theta-(poly(theta)/der(theta,fit))
    
    poly = np.poly1d(fit)
    # print(poly.r)
    theta=[]
    angle=0
    for i in poly.r:    #On fait défiler les racines
        if 0<i.real<90 and i.imag==0.0:     #On prend uniquemnt les raciens reelles
            theta.append(i.real)
    
    for i in theta: #On regarde quelles racines (et doncd quelle angle) convient !
        # print(testrajectoire(m,vitesse,i,vitessevent)[0][-1],"abscisse",absc[posj1],"posj1")
        if absc[posj1]-25<testrajectoire(m,vitesse,i,vitessevent)[0][-1]<absc[posj1]+25:
            # print(testrajectoire(m,vitesse,i,vitessevent)[0][-1],"abscisse",posj1,"posj1")
            return i
            
    return -1       #Si rien ne convient on renvoit -1, l'ia va devoir se debrouiller autrement ;)      
    
       
def angleIa(t):     #Calcul d'un angle optimale pour l'ia lorsqu'elle n'est pas en mode shooting en fonction du denivelé et du relief qui se dresse face à elle notamment
    global absc,im
    
    denivele=maxhauteurj2()-im[posj2]
    # print(denivele)
    distancemax=abs(absc[posj2]-absc[indicemaxhauteurj2()])
    # print(distancemax)
    oppose=0
    adjacent=0
    # print(denivele,distancemax,indicemaxhauteurj2(),"denivele")
    if denivele>20 and t=="n":
        oppose=denivele
        adjacent=distancemax
        angle=np.sin(oppose/adjacent)
        angle=(angle*360)/(2*pi)+10
    else:
        angle=35
    if t=="s":
        angle=15
        
    # print("angle",angle)
    
    return angle
    
#Fonctions annexes pour le calcul de l'angle
def maxhauteurj2():
    return max(im[200:posj2])
    
def indicemaxhauteurj2():
    return im.index(maxhauteurj2())
    
def maxhauteur():
    return max(im[0:posj2])
def indicemaxhauteur():
    return im.index(maxhauteur())

def denivelemap():
    return (max(im)-min(im))
    
def calculdistance():
    distance=abs(absc[posj1]-absc[posj2])
    return distance
    
def analyseia(posbo,vent,shoot):#Cerveau (assez primaire ;) ) de l'IA
    global statsvitesseanglej1
    angle,vitesse,projectile,deplacement,tricheur,enfer=0,0,0,0,False,False
    angle=angleIa("n")
    
    deplacement=randint(-20.0,20.0)
    # Comportement primaire    
    if calculdistance()>=800:
        projectile=0
        vitesse=randint(100.0,105.0)
        # print("Tir a longue distance")

    elif 500<calculdistance()<800:
        projectile=0
        vitesse=60+(calculdistance()/30)
        # print("Tir à distance intermediaire")
        
    elif 800<calculdistance()<400 and viej2<=viej1:
        projectile=2
        angle+=10
        vitesse=(calculdistance()/10)
        # print("Tir à distance intermediaire d'explosif")  
    
    else:
        projectile=2
        vitesse=randint(65.0,80.0)
        # print("Autre") 
         
    if len(impactj2[0])>0:
        if impactj2[0][-1]>absc[posj1]+200:
            deplacement=int((posj2-indicemaxhauteur())/2)
            # print("Avance vers max")  
            
    if 215<posbo<400:
        if posj2-posbo>=0:
            deplacement=int(posj2-posbo)+5
            # print("Avance vers bonus")
            angle-=deplacement*0.3
        else:
            deplacement=int(posj2-posbo)-5
            # print("Recule vers bonus")
            angle+=deplacement*0.3
    
            
    #Affinage du comportement primaire par observation du resultat precedent  
    if len(impactj2[0])>0:
        # print(impactj2[0][-1],absc[posj1])
        if (impactj2[0][-1]-absc[posj1])>+200:
            angle+=(impactj2[0][-1]-absc[posj1])/50
            # print("Rehausse tir")
            tricheur=False
        if (impactj2[0][-1]-absc[posj1])<-200:
            angle+=(impactj2[0][-1]-absc[posj1])/50
            # print("Rabaisse tir")
            tricheur=False
        if 0<impactj2[0][-1]-absc[posj1]<200:
            angle+=2.3
            # print("Rehausse tir")
            tricheur=False
        if -200<impactj2[0][-1]-absc[posj1]<0:
            angle-=2.3
            # print("Rabaisse tir")
            tricheur=False
        if  (impactj2[0][-1]-absc[posj1])<1:
            vitesse+=2   
                 
    if denivelemap()<100 and abs(im[posj2]-im[posj1])<50:
        angle=angleIa("s")
        vitesse=130
        projectile=1
        # print("Tir sniper")
        
        #Affinage du comportement primaire par observation du resultat precedent             
        if len(impactj2[0])>0:
            # print(impactj2[0][-1],absc[posj1])
            if impactj2[0][-1]>absc[posj1]:
                angle+=(impactj2[0][-1]-absc[posj1])/50
                # print("Rehausse tir")
                tricheur=False
            else:
                angle+=(impactj2[0][-1]-absc[posj1])/50
                # print("Rabaisse tir")
                tricheur=False
            
            if  (impactj2[0][-1]-absc[posj1])<1:
                vitesse+=2
                
    #Cas particuliers rangé par ordre d'importance (est donc le dernier executé est le plus important) 
    
    if touchéj1==True:
        if im[posj1]-30<im[posj2]<im[posj1]+30:
            vitesse=statsvitesseanglej1[0][-1]
            angle=statsvitesseanglej1[1][-1]
            angle=(angle*360)/(2*pi)
            projectile=choixproj1
            deplacement=0
            tricheur=True
            # print("Je recopie",vitesse,angle)
        else:
            deplacement=randint(-20.0,20.0)
        
    if len(impactj2[0])>0:    
        if absc[posj1]-25<=impactj2[0][-1]<=absc[posj1]+25 and im[posj1]<=impactj2[1][-1]<=im[posj1]+50 and viej1>70:
                angle=statsvitesseanglej2[1][-1]
                angle=(angle*360)/(2*pi)
                vitesse=statsvitesseanglej2[0][-1]
                projectile=choixproj2
                deplacement=0
                tricheur=True 
                # print("La meme") 
        
    if viej2<=20:        
        if posj2<indicemaxhauteurj2():
            deplacement=int((posj2-indicemaxhauteurj2())/2)+5
            # print("Fuite")
                

    if viej2>100 and viej2>viej1:
        enfer=True
        # print("Oui enfer")
    else:
        enfer=False
        # print("Non enfer")
        
    if shoot==True and ia=="c":   
        masse=statsproj[projectile][0]
        theta=shooting(masse,vitesse,0,vent[0])
        # print(masse,vitesse) 
        if theta!=-1:
            print("MODE SHOOTING ACTIVE")
            angle=theta
            # print(angle ,"angleia")
        
        
    return angle,vitesse,projectile,deplacement,tricheur,enfer

                 
## Fonctions de création de trajectoire et de vent 

       
def creationdetrajectoire(posx,posy,joueur,vent,posjadv,nomadv,angledeg,vitesse,positionbonus): #Fonction qui affiche la trajectoire du joueur
    global statsvitesseanglej1,statsvitesseanglej2,statsproj,choixproj1,choixproj2,puissancej1,puissancej2,bonusj1,bonusj2,ia   


    testpoint=False 
    
    if vitesse==0:      #Toujours le cas sauf quand on appelle les multitirs qui utilisent la vitesse du tir central ...
        if ia!="a" and joueur=='joueur2':
            angledeg,vitesse,choixproj2=analyseia(positionbonus,vent,True)[0:3]
            puissancej2=statsproj[choixproj2][2]
        else:
            choixproj=-1
            while 1:       #On choisit un projectile
                print("\n\noxoxoxoType projectile "+joueur+" ? oxoxoxo\n")
                print("1:Standard")
                print("2:Flèche")
                print("3:Explosif")
                choixproj=input("------>")
                if choixproj.isdigit():
                    choixproj=int(choixproj)-1 
                    if choixproj!=0 and choixproj!=1 and choixproj!=2:
                        print("invalide")
                    else:
                        break
                else:
                    print("entrez une des valeurs numériques proposées  svp")
            
            if joueur=='joueur1':       #On donne au joueur concerné le projectile en question
                choixproj1=choixproj
                puissancej1=statsproj[choixproj1][2]
            else:
                choixproj2=choixproj
                puissancej2=statsproj[choixproj2][2]
                
            rafraichir(vent,positionbonus,0,0)
                
            while 1:       #On demande au joueur de choisir une vitesse de tir qui doit être comprise entre les vitesses limites du projectiles
                print("\n\noxoxoxo Vitesse projectile "+joueur+" ? oxoxoxo\n")
                print("Vmin="+str(statsproj[choixproj][4]))
                print("Vmax="+str(statsproj[choixproj][5]))
                vitesse=input("------>")
                if isfloat(vitesse)==True:       #Barrière anti truand
                    vitesse=float(vitesse)
                    if vitesse<statsproj[choixproj][4] or vitesse>statsproj[choixproj][5]:
                        print("invalide")
                    else:
                        break
                else:
                    print("entrez une valeur numérique svp")
                    
            while 1:    
                print("\n\noxoxoxo Angle projectile "+joueur+" ? oxoxoxo\n")        #On demande de choisir un angle de tir
                angledeg=input("------>")
                if isfloat(angledeg)==True: 
                    angledeg=float(angledeg)
                    break
                else:
                    print("entrez une valeur numérique svp")
                
            
    # print(angledeg)
    angle=convertionangle(angledeg)
    
    if joueur=='joueur1':           #On modifie les dégats du projectile si le bonus en cause est activer**é
        if bonusj1==10 or bonusj2==11:
            degatupdown()
            bonusj1=-1
    else:
        if bonusj2==10 or bonusj2==11:
            degatupdown()
            bonusj2=-1
        
    rafraichir(vent,positionbonus,0,0)
    
    if joueur=="joueur1":       
        vitessevent=vent[0]         #On récupère le vent qui entre dans l'équation des projectiles
        statsvitesseanglej1[0].append(vitesse) #On récupère la vitesse du joueur est l'angle de tir pour les stats finales
        statsvitesseanglej1[1].append(angle)
        statsventprojectile[0]+=1       #et un projectile de plus tiré ... pour les stats finales
        k=statsproj[choixproj1][1]      #On modifie le coefficient de frottement et la masse du projectile, ceux du projectile choisi
        m=statsproj[choixproj1][0]
    else:       #Même chose pour j2
        vitessevent=-vent[0]
        caractvent=vent[1]
        statsvitesseanglej2[0].append(vitesse)
        statsvitesseanglej2[1].append(angle)
        statsventprojectile[1]+=1
        k=statsproj[choixproj2][1]
        m=statsproj[choixproj2][0]
    
    # print(k,m)    
    pas=0.1     #Euler quoi ...
    g=9.81
    
    vx = vitesse* cos(angle)
    x=posx
    vy = vitesse* sin(angle) 
    y=posy
   
    tabvx=[vx]
    tabx=[x] 
    tabvy=[vy]
    taby=[y]
    
    i=0
    while (testpoint==False and min(im)<=y): #On trace la trajectoire selon euler
        vxold=vx
        xold=x
        vyold=vy
        yold=y
        vx=vxold+pas*(-(k/m)*((sqrt((vyold)**2+(vxold-vitessevent)**2))*(vxold-vitessevent)))
        vy=vyold+pas*(-g-(k/m)*((sqrt((vyold)**2+(vxold-vitessevent)**2))*(vyold)))
        
        # vx=vxold+pas*(-(k/m)*(vxold-vitessevent)**2) #il aurait été plus correct de l'écrire comme ca : vx=vxold+pas*(-(k/m)*(((sqrt(vyold**2+vxold**2)))*vxold) , c'est la vraie intégration de l'équation avec frottement quadratique
        # vy=vyold+pas*(-g-(k/m)*(vyold-vitessevent)**2)# mais cette écriture simplifiée est plus pratique pour la modélistaion de la force du vent est donne des résultats quasi identiques dans les conditions du jeu
       
        if joueur=="joueur1":       #On augmente l'abscisse si c'est le projectile du joueur sinon on la diminue
            x=xold+vxold*pas  
        else:
            x=xold-vxold*pas 
            
        y=yold+vyold*pas 
        
        tabvx.append(vx)
        tabx.append(x) 
        tabvy.append(vy)
        taby.append(y)
        i+=1
        testpoint=testpointvalide(x,y,posjadv,nomadv)  
    
    impactfinal(tabx,taby,joueur)

        
    # print(puissancej1,puissancej2)
    
    return tabx,taby,vitesse,angledeg


def creationvent():         #Fonction qui génère un vent de face ou de dos entre 0 et 40m/s
    vitessevent=uniform(0.0,40.0)
    sens=choice([-1.0,1.0])
    caractvent=""
    beaufort=["Calme","Très légère brise","Légère brise","Petite brise", "Jolie brise","Bonne brise","Vent frais","Grand frais","Coup de vent","Fort coup de vent" ,"Tempête","Violente tempête","Ouragan"]
    intbeaufort=[[0.0,0.3],[0.3,1.5],[1.5,3.4],[3.4,5.4],[5.4,7.9],[7.9,10.7],[10.7,13.8],[13.8,17.1],[17.1,20.7],[20.7,24.4],[24.4,28.5],[28.5,32.7],[32.7,40.1]]
    for i in range(0,13,1):
        if intbeaufort[i][0]<=vitessevent<intbeaufort[i][1]:
            caractvent=beaufort[i]
    vitessevent=vitessevent*sens
    # print(vitessevent,caractvent)
    
    statsventprojectile[2].append(vitessevent)
    
    return vitessevent,caractvent #Renvoit la vitesse et une qualification de la force du vent donnée par l'échelle de beaufort       

        
##Fonction gérant les déplacements


def deplacement(j,vent,positionbonus):#Fonction de déplacement des joueurs sur la map
    
    global posj1, posj2, deplacementj1, deplacementj2, bonusj1, bonusj2,distanceparcourue,ia    #Variables globales qui prennent la position (en fait on les utilise comme indice des listes absc et im : soit posj1 =400, par exemple on pourra placer unc char placé en (absc[200], im[200]), il se situera au centre de la courbure, car on le rappel, la courbure est définie par 400 points
    pos=0
    mouvement=""
    
    if j=="joueur1":     #On gére soit les déplacements du joueur1 soit ceux du joueurs 2
        pos=posj1
        deplacement=deplacementj1
    else:
        pos=posj2
        deplacement=deplacementj2
    
    if ia!="a"  and j=="joueur2":
        nombremouvement=analyseia(positionbonus,vent,False)[3]
    else:
        while 1:
            print("\n\noxoxoxo Nombre de mouvement "+j+"? (une unité de déplacement vaut 5 m ) oxoxoxo\n")
            print("Déplacement positif pour avancer, négatif pour reculer\n")
            nombremouvement=input("------>")       #Nombre d'unité de déplacement dont veux se déplacer le joueur (une unité vaut à peu près 5m)
            if isint(nombremouvement)==True:
                nombremouvement=int(nombremouvement)
                break
            else: 
                print("entrez une valeur entière svp")
    
    pas=0 
    for i in range(1,deplacement+1):   
        if i>abs(nombremouvement) : #Si le nombre de déplacement voulue par le joueur dépasse son nombre de déplacement limite, on stoppe sa course une fois toute ses unités utilisées
            break    
             
        if nombremouvement>0:
            if ((pos-1)<217 and j=="joueur2" ) or ((pos+1)>183 and j=="joueur1") :#condition nécessaire si on suppose que le joueur ne peut aller au dela de l'eau (joueur1) et de l'eau (joueur2)
                break
            else:
                if j=="joueur1":
                    pos+=2 
                if j=="joueur2":
                    pos-=2 
        elif nombremouvement<0:
            if  ((pos+1)>387 and j=="joueur2") or ((pos-1)<10 and j=="joueur1"):#condition nécessaire si on suppose que le joueur ne peut aller au dela de l'origine[0,0] (joueur2) et de la map (joueur1)
                break
            else:
                if j=="joueur1":
                    pos-=2 
                if j=="joueur2": 
                    pos+=2  
        else:
            break
        
           
        if j=="joueur1":     #On récupére la nouvelle position du joueur
            posj1=pos
            if absc[positionbonus]-25<absc[posj1]<absc[positionbonus]+25:        #Si elle correspond à celle du bonus, il s'arrète (break), un bonus est tiré au hasard (uniform...) est la machine à bonus s'occupe de le recompenser si le bonus a une action immédiate
                bonusj1=int(uniform(0.0,12.0))
                machineabonus(bonusj1,j,vent,positionbonus)
                #print("touché",bonusj1)
                break
        else:
            posj2=pos
            if absc[positionbonus]-25<absc[posj2]<absc[positionbonus]+25:
                bonusj2=int(uniform(0.0,12.0))
                machineabonus(bonusj2,j,vent,positionbonus)
                #print("touché",bonusj2)
                break
                
        rafraichir(vent,positionbonus,0,0)
        pas+=1
    
    if j=="joueur1":        #Nombre de déplacement pour les stats
        distanceparcourue[0]+=pas*5
    else:
        distanceparcourue[1]+=pas*5
      
   
## Fonctions pour le tableau des stats

def impactfinal(x,y,joueur):  #On récupère la coordonnée des derniers points de chaque trajectoire pour les stats
    
    global impactx, impacty
    
   
    if joueur=="joueur1":
        impactj1[0].append(x[-1])
        impactj1[1].append(y[-1])
    else:
        impactj2[0].append(x[-1])
        impactj2[1].append(y[-1])    

    # print(impactj1,impactj2)
    
def stats():        #Fonction qui affiche plein de petits graphiques résumant la partie ;) 
    
    fig =figure()       #Nouvelle fenêtre qui s'affiche en fin de partie avec les stats
    im9=mpimg.imread("L'artilleur.png")     #On charge une image de la map en fin de partie
    fig.subplots_adjust(bottom=0.025, left=0.025, top = 0.975, right=0.975)     #   Plus très utile ici mais permettait de placer les petites fenetres dans la fenetre principale
    
    with plt.xkcd():        # Contexte manager, décoratif, modifie le style des graphiques. Celui ci donne un petit coté dessin à la main aux stats bien sympa ;)
    
## Graphe 1, on affiche l'étendu des dégats
        ax1 = fig.add_axes((0.01, 0.52, 0.50, 0.50)) #On place l'image à un emplacement bien particulier (x1,y1,x2,y2)
        xticks([]), yticks([])      #On retire les axes (inutile ici je pense)
        
        ax1.imshow(im9) 
        
        taille=shape(im1)       #Plus utilisé ...
        

## Graphe 2, on affiche le pourcentage de tir réussi et de tir manqué du joueur 1
    
        ax2 = fig.add_axes((0.05, 0.29, 0.2, 0.2))
        xticks([]), yticks([])
        plt.title("Tir joueur 1",size=10)
        
        ratéj1=str((statsventprojectile[0])-tirreussi[0])
        reussij1=str(tirreussi[0])
        
        nom = ['Touché', 'Manqué']
        toucheratej1 = [reussij1,ratéj1]
        
        couleurs = ['gold', 'lightskyblue']     #Couleurs des deux parts de camembert
        
        decalage=(0, 0.15)   #Décalage entre deux parts de camembert
        ax2.pie(toucheratej1 , explode=decalage, labels=nom,colors=couleurs, autopct='%1.1f%%', startangle=90, shadow=True)      #On affiche le graphe camembert
        plt.axis('equal')       #On adapte la taille
        
        # print(statsventprojectile,tirreussi)
        

## Graphe 3, on affiche le pourcentage de tir réussi et de tir manqué du joueur 2
        
        ax3 = fig.add_axes((0.3, 0.29, 0.2, 0.2))
        xticks([]), yticks([])
        plt.title("Tir joueur 2",size=10)
        
        ratéj1=str((statsventprojectile[1])-tirreussi[1])
        reussij1=str(tirreussi[1])
        
        nom = ['Touché','Manqué' ]
        
        toucheratej2 = [reussij1,ratéj1]
        couleurs = ['gold', 'lightskyblue']
        
        decalage=(0, 0.15)
        
        ax3.pie(toucheratej2 , explode=decalage, labels=nom,colors=couleurs, autopct='%1.1f%%', startangle=90, shadow=True)
        plt.axis('equal')
        
## Graphe 4, on affiche la répartition des bonus attrapés par les joueurs      
        
        if choix3=="a" and (statbonus[0]>0 or statbonus[1]>0):
            
            ax4= fig.add_subplot(339, axisbg='#FF0033')
            xticks([]), yticks([])
            plt.title("Bonus")
            
            nom = ['Joueur 1', 'Joueur 2']
            toucheratej1 = [str(statbonus[0]),str(statbonus[1])]
            
            couleurs = ['#FF6969', '#6050DC']       #Couleur en hexa pour changer ;)
            
            decalage=(0, 0.15)
            ax4.pie(toucheratej1 , explode=decalage, labels=nom,colors=couleurs, autopct='%1.1f%%', startangle=90, shadow=True)
            plt.axis('equal')
    
## Graphe 5, on affiche le nombre de déplacement de chaque joueur dans un graphique baton
    
        ax5 = fig.add_axes((0.09, 0.05, 0.25, 0.2))
        ax5.bar([-0.125, 0.0 - 0.125], [0, distanceparcourue[0]], 0.25,facecolor='#9999ff', edgecolor='white')
        ax5.bar([-0.125, 1.0 - 0.125], [0, distanceparcourue[1]], 0.25,facecolor='#9999ff', edgecolor='white')
        
        
        plt.ylabel('DISTANCE PARCOURUE', size=10)
        
        ax5.set_xticks([0, 1])
        ax5.set_xlim([-0.5, 1.5])
        ax5.set_ylim([0, max(distanceparcourue)+50])
        ax5.set_xticklabels(['DISTANCE \nJOUEUR 1', 'DISTANCE \nJOUEUR 2'], size=5)
        
## Graphe 6, on affiche des infos en plus relatives à la partie  
    
        eqs = []
        
        nombredecoupdevent=statsventprojectile[2]
        moy=int(moyenne(nombredecoupdevent))
        
        
        eqs.append(("Vitesse moyenne\n"+ "du vent : "+str(moy)+ " m/s"))
        eqs.append(("\nDurée de la partie : "+str(int(temps))+" s"))
        eqs.append(("\nProjectiles tirés : "+str(statsventprojectile[0]+statsventprojectile[1])))
        
        axes([0.37,0.05,0.3,0.2])
    
    
    
    text(0.5, 0.7, eqs[0], ha='center', va='center', color="#11557c",transform=gca().transAxes, fontsize=10, clip_on=True)
    text(0.5, 0.5, eqs[1], ha='center', va='center', color="#11557c",transform=gca().transAxes, fontsize=10, clip_on=True)
    text(0.5, 0.3, eqs[2], ha='center', va='center', color="#11557c",transform=gca().transAxes, fontsize=10, clip_on=True)
    xticks([]), yticks([])
    
## Graphe 7, on affiche la vitesse de chaque projectile ainsi que l'angle de tir choisi (enfin ceux ne dépassant pas 175 m/s .... normalement impossible)
    
    ax4 = fig.add_axes((0.45, 0.35, 0.6, 0.6), projection='polar')
    
    rj1 =np.array(statsvitesseanglej1[0])
    rj2 =np.array(statsvitesseanglej2[0])
    
    thetaj1 = np.array(statsvitesseanglej1[1])
    thetaj2 = np.array(statsvitesseanglej2[1])
    
    
    ax4.scatter(thetaj1, rj1, c="red", s=50, cmap=plt.cm.hsv)
    ax4.scatter(thetaj2, rj2, c="blue", s=50, cmap=plt.cm.hsv)
    ax4.set_alpha(0.75)
    
    # print(distanceparcourue)
    plt.ylim(0,175)  #On fixe les axes en fonction notamment de la valeur minimum et maximum de la hauteur de la map (ordonnées im)
    plt.xlim((0,175))
    
    
    plt.show()
    
## Début du programme


im1=mpimg.imread('charj1.png') #Chargement des images des différentes entités
im2=mpimg.imread('charj2.png') 
im1bis=mpimg.imread('catapultej1.png')
im2bis=mpimg.imread('catapultej2.png') 
im3=mpimg.imread('fond1.png') 
im4=mpimg.imread('explosion.png') 
im5=mpimg.imread("croix-rouge.png") 
im6=mpimg.imread("Bonus.png")
im7=mpimg.imread("atomique.png")
im8=mpimg.imread("Gouttedeau.png")
im9=mpimg.imread("verj1.png")
im10=mpimg.imread("verj2.png")  

fig = plt.figure()      #Création de la fenetre

fig.patch.set_facecolor('#FF0033') #Permet de changer la couleur des bordures de la fenetre
ax= fig.add_subplot(111, axisbg='#FF0033')#On crée une seule division de la fenetre(essayer 211)

ax.axes.get_xaxis().set_visible(False)      #Efface les axes
ax.axes.get_yaxis().set_visible(False)


creationmap()   #On génére la map

vent=[0,""]      #Variable qui va récupérer la vitesse du vent
positionbonus=200  #Position du bonus au début de la prtie, au centre de la map
rafraichir(vent,positionbonus,0,0)


plt.ylim((min(im)-50,min(im)+600))  #On fixe les axes en fonction notamment de la valeur minimum de la hauteur de la map (ordonnées im)
plt.xlim((0,1000.0))

# F = gcf()
# fig.set_size_inches(18.5, 10.5, forward=True)
#Desactivé, permet d'afficher tout en pleine page, coute chère en ressource (gros ralentissement à prévoir :) )

choix=menu()        #On appelle le menu du jeu
choix1=choix[0]
choix2=choix[1]
choix3=choix[2]


if choix2=="b":     #Si on choisit de joueur avec vent
    vent=creationvent()
if choix3=="a":   #Si on choisit de joueur avec bonus
    positionbonus=bonus()
        
   
while(viej1>0 and viej2>0):
    rafraichir(vent,positionbonus,0,0) 
    #print(bonusj1,bonusj2)
    if choix3=="a":     #Si on choisit de joueur avec bonus
        if bonusj1==-1 or bonusj2==-1:  #Et que des bonus ont été pris au tour précédent
            positionbonus=bonus()       #On en replace un nouveau sur la map
            bonusj1=40
            bonusj2=40
    if choix2=="a":  #Si on choisit de joueur avec vent DIFFERENT à chaque tour
       vent=creationvent() 
    rafraichir(vent,positionbonus,0,0)
    Jeu(choix1,vent,positionbonus)          #On appelle la fonction centrale du programme 
    rafraichir(vent,positionbonus,0,0) 
    
if viej1>viej2:
    print(" Le joueur 1 a gagné ! ")
elif viej2>viej1:
    print(" Le joueur 2 a gagné ! ")
else:
    print(" Egalité ! ")
    
end = time.time()       #On arrète le timer
temps=(end - start)

#Ici on place l'ensemble des projectiles tirés au cours de la partie sur la map, on enregistre le tout, cette image sera celle affichée dans les stats !

plt.plot(impactj1[0],impactj1[1], 'bo', ms=7,zorder=4,color= "red")         
plt.plot(impactj2[0],impactj2[1], 'bo', ms=7,zorder=4,color= "blue") 

#print(impactj1,impactj2)

extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
plt.savefig("L'artilleur", bbox_inches=extent)

plt.close()

stats()#On appelle les stats !


    
    







