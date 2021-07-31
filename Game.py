# -*- coding: utf-8 -*-

import random as rd
import os
import numpy as np
import pygame
from pygame.locals import *
import Shapes as Shp
import sys

#Fonctions :

def collision():
    """
    Vérifie si la pièce repose sur une autre pièce ou le bas de l'écran.
    """
    global grille
    for ligne in range(22):
        for colonne in range(10):
            if type(grille[ligne][colonne]) is str:
                
                if ligne+1 == 22:
                    return True
                
                bottomtile = grille[ligne+1][colonne]
                if type(bottomtile) is int and bottomtile != 0:
                    return True
                
    return False

def ClearLines():
    """
    Enlève les lignes complérées et incrémente le score.
    """
    global grille
    global Score
    NbLines = 0
    for i in range (22) :
        line = grille[i]
        
        Hole = False
        for j in line :
            if j == 0 :
                Hole = True

        if not Hole :
            NbLines += 1
            Score += NbLines*50
            for k in range (i-1) :
                grille[i-k] = grille[i-k-1].copy()

    return None

def shapeingrill():
    """
    Permet d'introduire chaque bloc de la forme en jeu dans le tableau principal en retirant ceux de la position précédente.
    """
    global grille
    global SHAPE
    global x
    global y
    for ligne in range(22):
        for colonne in range(10):
            if type(grille[ligne][colonne]) is str :
                grille[ligne][colonne] = int(0)

    for line in range(4):
        if y+line >= 0 :
            for column in range(4):
                if SHAPE[line][column] != '' :
                    grille[y+line][x+column] = str(SHAPE[line][column])
    return None

def printin():
    """
    Affiche le contenu du tableau principal sur l'écran.
    """
    global grille
    Fenetre.blit(Fond, (0, 0))
    offsetx, offsety = 113, 31
    for ligne in range(22):
        for colonne in range(10):
            if type(grille[ligne][colonne]) is str :
                Rect = pygame.Rect(offsetx+delta*colonne, offsety+delta*ligne, delta, delta)
                pygame.draw.rect(Surface, (255, 255, 255), Rect)
                #exterieur blanc pour la pièce en jeu
            elif grille[ligne][colonne] != 0 :
                Rect = pygame.Rect(offsetx+delta*colonne, offsety+delta*ligne, delta, delta)
                pygame.draw.rect(Surface, (0, 0, 0), Rect)
                #exterieur noir pour les pièces déjà posées
            if int(grille[ligne][colonne]) != 0 :
                Rect = pygame.Rect(offsetx+delta*colonne+1, offsety+delta*ligne+1, delta-2, delta-2)
                color = colors[int(grille[ligne][colonne])]
                pygame.draw.rect(Surface, (color), Rect)
                #intérieur de couleur pour toutes les pièces selon leur forme initiale

    if hold != 7 :
        Fenetre.blit(image[hold], (7, 31))

    Fenetre.blit(image[nxtshapes[1]], (319, 31))

    for i in range(2, 5):
        Fenetre.blit(image[nxtshapes[i]], (319, 81*i-32))

    text = font.render("Score : "+str(Score), True, (0, 0, 0))
    Fenetre.blit(text, (118, 0))
    
    pygame.display.flip()
    return None

#Génération aléatoire des tétrominos :

Rot = 0

Baba = [i for i in range(7)]
nxtshapes = [rd.choice(Baba)]
listshapes = Baba.copy()
for i in range(4) :
    listshapes.remove(nxtshapes[-1])
    nxtshapes.append(rd.choice(listshapes))

SHAPE = Shp.Shapes[4*nxtshapes[0]]

#Initialisation des variables et du tableau :

h, w = 22, 10
you = ['player']
delta = 20
delay = 1000
Score = 0
ScoreStep = 0
x, y = 3, -4
if nxtshapes[0] == 3 :
    y = -3

hold = 7
HOLD = False

grille = [[0 for i in range(w)] for j in range(h)]
##print(np.array(grille, dtype = 'int'))
colors = [(153, 217, 234), (0, 172, 238), (29, 117, 187), (246, 147, 32), (255, 241, 0), (139, 197, 63), (101, 45, 144), (236, 27, 36)]

LOSE = False

#Importation des images :

Fond = pygame.image.load(os.path.join("images\Fond.png"))
I = pygame.image.load(os.path.join("images\I.png"))
J = pygame.image.load(os.path.join("images\J.png"))
L = pygame.image.load(os.path.join("images\L.png"))
O = pygame.image.load(os.path.join("images\O.png"))
S = pygame.image.load(os.path.join("images\S.png"))
T = pygame.image.load(os.path.join("images\T.png"))
Z = pygame.image.load(os.path.join("images\Z.png"))

image = [I, J, L, O, S, T, Z]

#Initialisation de pygame :

pygame.init()

Fenetre = pygame.display.set_mode((426, 486))
Surface = pygame.display.get_surface()

continuer = True

pygame.key.set_repeat(100, 20)

#Réglages du texte :

all_fonts = pygame.font.get_fonts()
if "comicsansms" in all_fonts :
    font = pygame.font.SysFont("comicsansms", 24)
else :
    font = pygame.font.Font(None, 40)

losetext = font.render("You lost, press Spacebar to try again", True, (0, 0, 0))
pausetext1 = font.render("Pause", True, (0, 0, 0))
pausetext2 = font.render("press escape to return to the game", True, (0, 0, 0))

#Rendu de la grille :

printin()

#Création de la boucle créant un délai de 0.8s et guettant les évènements :

while continuer:
    time = pygame.time.get_ticks()
    Nbevents = 0
    while pygame.time.get_ticks()-time < delay :
        event = pygame.event.get()
        
        if len(event) != 0 :
            event = event[0]

            if event.type == QUIT :
                continuer = False

            if event.type == KEYDOWN :

                Nbevents += 1
                isOOB = False

#Rotation horraire et réctification de la position :

                if event.key == K_d :
                    Rot += 1
                    if Rot == 4 :
                        Rot = 0
                    done = False
                    NbTry = 0
                    basex, basey = x, y
                    while not done and not isOOB :
                        SHAPE = Shp.Shapes[4*nxtshapes[0]+Rot]
                        OUT = False
                        line = 0
                        while line < 4 and not OUT :
                            column = 0
                            while column < 4 and not OUT :
                                if SHAPE[line][column] != '' :
                                    if x+column > 9 or x+column < 0 or y+line > 21 :
                                        tile = 1
                                    elif y+line < 0 :
                                        tile = 0
                                    else :
                                        tile = grille[y+line][x+column]

                                    if type(tile) is int and tile != 0:
                                        if NbTry == 0 :
                                            x += 1
                                            OUT = True
                                            NbTry += 1
                                        elif NbTry == 1 :
                                            x -= 2
                                            OUT = True
                                            NbTry += 1
                                        elif NbTry == 2 :
                                            x, y = x+1, y+1
                                            OUT = True
                                            NbTry += 1
                                        elif NbTry == 3 :
                                            y -= 2
                                            OUT = True
                                            if np.all(SHAPE == Shp.I_1) or np.all(SHAPE == Shp.I_3) :
                                                NbTry += 1
                                            else :
                                                NbTry = 6
                                        elif NbTry == 4 :
                                            y += 1
                                            x += 2
                                            OUT = True
                                            NbTry += 1
                                        elif NbTry == 5 :
                                            x -= 4
                                            OUT = True
                                            NbTry += 1
                                        elif NbTry == 6 :
                                            x, y = basex, basey
                                            Rot -= 1
                                            if Rot == -1 :
                                                Rot = 3
                                            SHAPE = Shp.Shapes[4*nxtshapes[0]+Rot]
                                            OUT = True
                                            isOOB = True
                                            
                                column += 1
                            line += 1                 
                        if not OUT :
                            done = True

                    if not isOOB:
                        time = pygame.time.get_ticks()-(delay/10)*Nbevents

#Rotation anti-horraire et réctification de la position :
                        
                if event.key == K_a :
                    Rot -= 1
                    if Rot == -1 :
                        Rot = 3
                    done = False
                    NbTry = 0
                    basex, basey = x, y
                    while not done and not isOOB :
                        SHAPE = Shp.Shapes[4*nxtshapes[0]+Rot]
                        OUT = False
                        line = 0
                        while line < 4 and not OUT :
                            column = 0
                            while column < 4 and not OUT :
                                if SHAPE[line][column] != '' :
                                    if x+column > 9 or x+column < 0 or y+line > 21 :
                                        tile = 1
                                    elif y+line < 0 :
                                        tile = 0
                                    else :
                                        tile = grille[y+line][x+column]

                                    if type(tile) is int and tile != 0:
                                        if NbTry == 0 :
                                            x += 1
                                            OUT = True
                                            NbTry += 1
                                        elif NbTry == 1 :
                                            x -= 2
                                            OUT = True
                                            NbTry += 1
                                        elif NbTry == 2 :
                                            x, y = x+1, y+1
                                            OUT = True
                                            NbTry += 1
                                        elif NbTry == 3 :
                                            y -= 2
                                            OUT = True
                                            if np.all(SHAPE == Shp.I_1) or np.all(SHAPE == Shp.I_3) :
                                                NbTry += 1
                                            else :
                                                NbTry = 6
                                        elif NbTry == 4 :
                                            y += 1
                                            x += 2
                                            OUT = True
                                            NbTry += 1
                                        elif NbTry == 5 :
                                            x -= 4
                                            OUT = True
                                            NbTry += 1
                                        elif NbTry == 6 :
                                            x, y = basex, basey
                                            Rot += 1
                                            if Rot == 4 :
                                                Rot = 0
                                            SHAPE = Shp.Shapes[4*nxtshapes[0]+Rot]
                                            OUT = True
                                            isOOB = True

                                column += 1
                            line += 1                    
                        if not OUT :
                            done = True

                    if not isOOB:
                        time = pygame.time.get_ticks()-(delay/10)*Nbevents

#Translation vers la droite et vérification des collisions :
                        
                if event.key == K_RIGHT :
                    x += 1
                    for line in range(len(SHAPE)):
                        for column in range(len(SHAPE[line])):
                            if SHAPE[line][column] != '' :
                                if x+column > 9:
                                    isOOB = True
                                    x -= 1

                                if y+line >= 0 :
                                    tile = grille[y+line][x+column]
                                    if type(tile) is int and tile != 0 :
                                        isOOB = True
                                        x -= 1

                    if not isOOB:
                        time = pygame.time.get_ticks()-(delay/10)*Nbevents

#Translation vers la gauche et vérification des collisions :
                        
                if event.key == K_LEFT :
                    x -= 1
                    for line in range(len(SHAPE)):
                        for column in range(len(SHAPE[line])):
                            if SHAPE[line][column] != '' :
                                if x+column < 0:
                                    isOOB = True
                                    x += 1

                                if y+line >= 0 :
                                    tile = grille[y+line][x+column]
                                    if type(tile) is int and tile != 0 :
                                        isOOB = True
                                        x += 1
                                    
                    if not isOOB:
                        time = pygame.time.get_ticks()-(delay/10)*Nbevents

#Accélération manuelle du tétromino par le joueur :
                        
                if event.key == K_DOWN :
                    time = pygame.time.get_ticks()-delay

#Échange entre la pièce en jeu et la pièce en réserve :

                if event.key == K_h and not HOLD:
                    time = pygame.time.get_ticks()
                    
                    if hold == 7 :
                        listshapes = Baba.copy()
                        for shape in nxtshapes :
                            listshapes.remove(shape)
                        nxtshapes.append(rd.choice(listshapes))
                        hold = nxtshapes.pop(0)
                    else :
                        tempshape = nxtshapes[0]
                        nxtshapes[0] = hold
                        hold = tempshape

                    Rot = 0
                    x, y = 3, -3
                    if nxtshapes[0] == 3 :
                        y = -2
                    
                    SHAPE = Shp.Shapes[4*nxtshapes[0]]
                    HOLD = True

#Pause :
                if event.key == K_ESCAPE :
                    pygame.key.set_repeat(500, 100)
                    Fenetre.blit(pausetext1, (213-pausetext1.get_width()//2, 200))
                    Fenetre.blit(pausetext2, (213-pausetext2.get_width()//2, 220))
                    pygame.display.flip()
                    pause = True
                    while continuer and pause :
                        event = pygame.event.get()
                        
                        if len(event) != 0 :
                            event = event[0]

                            if event.type == QUIT :
                                continuer = False

                            if event.type == KEYDOWN :
                                if event.key == K_ESCAPE :
                                    pause = False
                    pygame.key.set_repeat(100, 20)

#Actualisation de la grille et affichage :
                    
                shapeingrill()
                printin()

#Vérification de la position du tétromino (fin de course) et génération du suivant

    if collision():
        if Baba is you :
            Cake = False
        for ligne in range(h):
            for colonne in range(w):
                grille[ligne][colonne] = int(grille[ligne][colonne])

        for line in range(4):
            for column in range(4):
                if SHAPE[line][column] != '' and y+line < 0 :
                    LOSE = True
                    

        if not LOSE :
            ClearLines()
            listshapes = Baba.copy()
            for shape in nxtshapes :
                try :
                    listshapes.remove(shape)
                except :
                    None
            nxtshapes.append(rd.choice(listshapes))
            nxtshapes.pop(0)
            Score += 10
            Rot = 0
            x, y = 3, -3
            if nxtshapes[0] == 3 :
                y = -2
            if Score > ScoreStep+500 :
                ScoreStep += 500
                if delay > 250 :
                    delay -= 50
                if delay > 50 :
                    delay -= 10
            
            SHAPE = Shp.Shapes[4*nxtshapes[0]]

        else :
            Fenetre.blit(losetext, (213-losetext.get_width()//2, 243-losetext.get_height()//2))
            pygame.display.flip()
            Restart = False
            while not Restart :
                for event in pygame.event.get() :
                    if event.type == KEYDOWN :
                        if event.key == K_SPACE :
                            Restart = True
                    if event.type == QUIT :
                        pygame.quit()
                        sys.exit()

#Réinitialisation de la grille :

            prvsScore = -1
            Score = 0
            Rot = 0
            x, y = 3, -4
            grille = [[0 for i in range(w)] for j in range(h)]
            nxtshapes = [rd.choice(Baba)]
            listshapes = Baba.copy()
            for i in range(4) :
                listshapes.remove(nxtshapes[-1])
                nxtshapes.append(rd.choice(listshapes))
            SHAPE = Shp.Shapes[4*nxtshapes[0]]
            if nxtshapes[0] == 3 :
                y = -3
            LOSE = False
            delay = 1000

        HOLD = False
        
    else :
        y += 1

#Actualisation de la grille et affichage :
        
    shapeingrill()
    printin()

pygame.quit()
