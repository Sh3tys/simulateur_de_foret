# Adapté du travail de Grégory Coutable 2022
# Partage sous licence Creative Commons :
# https://creativecommons.org/licenses/by-sa/3.0/fr/

import pygame
from pygame.locals import *
#pour le rendre dispo de n'importe où
import os
pathname = os.path.dirname(__file__)

class GUIsimulation (object):
    
    def __init__(self, nb, w):
        """
        Initialise une grille rectangulaire de nb * nb cases.
       
        """
        
        #des constantes pour le dessin de la grille
        self.nbx = nb #la taille de la grille
        self.nby = nb #la taille de la grille
        self.w = w #largeur d'une case
        self.d = self.w // 10 #entre deux cases
        self.wPol = int(self.w / 1.5) #taille de base des polices
        self.wPol2 = (nb * w) // 10 
        #la liste des coordonnées de chaque case de la grille (coordonnées du coin en haut à gauche)
        self.xy0 = [self.d + (self.d + self.w) * x for x in range(self.nbx)]

        #initialisation de pygame
        pygame.init()
        #calcul de la taille totale de la fenêtre
        self.wFen = self.nbx * self.w + (self.nbx + 1) * self.d
        #hauteur idem + un bandeau pour le score
        self.hBandeau = 0 #100 à l'origine
        hFen = self.nby * self.w + (self.nby + 1) * self.d + self.hBandeau
        self.rectG = pygame.Rect(0, 0, self.wFen //3, self.hBandeau)
        self.rectC = pygame.Rect(self.wFen //3, 0, self.wFen //3, self.hBandeau)
        self.rectD = pygame.Rect(2*self.wFen //3, 0, self.wFen //3, self.hBandeau)
        #on définit la fenêtre de base de notre jeu
        self.fond = pygame.display.set_mode((self.wFen, hFen))
        #un titre sur cette fenêtre
        pygame.display.set_caption("Simulation de feu de forêt.")

        #une liste contenant les différentes cases possibles de vide à 32768
        self.cases = [self._creerCase(i) for i in range(0, 4)]
        
        self.memoGrille = [[-1 for x in range(self.nbx)] for y in range(self.nby)]
        
        self._enableTime = False
        
        
        self.refresh(self.memoGrille)
    
    def _creerCase(self, n):
        """
        Créé les cases pour le jeu : il en existe 4 différentes selon la valeur de n :
        0: terrain nu
        1: arbre vivant
        2: arbre en feu
        3: arbre en cendre
        """
        clrCase = ['#FFFFD4', '#00FF00', '#FF0000', '#646464'] #Couleur des 4 états des arbres

        case = pygame.Surface((self.w, self.w))
            
        case.fill(pygame.Color(clrCase[n]))         
            
        return case
    
    def refresh(self, g):
        """
        Cette méthode rafraichie l'affichage du démineur conformément à la grille passée en argument.
        
        g est une liste de nb listes.

        Le contenu de la grille définit le dessin de la case :
            0 à 3 : Terrain nu, arbre en vie, arbre en feu, arbre en cendre        
        """
        self.memoGrille = g

        self.fond.fill(pygame.Color("#BCAF9F"))
        for y in range(self.nby):
            for x in range(self.nbx):
                self.fond.blit(self.cases[g[y][x]], (self.xy0[x], self.xy0[y] + self.hBandeau)) 

     
        #Rafraîchissement de l'écran
        pygame.display.update()

    
        
    def waitClick(self):
        """
        Cette méthode attend l'action de l'utilisateur. Types d'actions :
            - demande fermeture de la fenètre : fermeture propre de la fenètre pygame et fin du programme python.
            - click sur la fenetre : retourne un tuple contenant les numéros (x, y, bouton) de la case choisie.
                Bouton fait référence au click souris : 'D' pour droit, 'G' pour gauche.
            - laché du bouton gauche de la souris : retourne 'G'
            - Quelques autres touches sont également gérées et retourne la lettre saisie.
        Une fois exécutée, on ne peut sortir de cette méthode que par l'une de ces actions.

        """        
        while True:
            #Limitation de vitesse de la boucle
            pygame.time.Clock().tick(30)

            for event in pygame.event.get():    #Attente des événements
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:   #Si clic gauche ou droit
                        if event.pos[1] > self.hBandeau:
                            return (event.pos[0]//(self.w + self.d), (event.pos[1] - self.hBandeau)//(self.w + self.d), ('G', 'C', 'D')[event.button - 1])
                
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    #detecte le relachement du click gauche
                        if event.pos[1] > self.hBandeau:
                            return (event.pos[0]//(self.w + self.d), (event.pos[1] - self.hBandeau)//(self.w + self.d), 'R')

                
                if event.type == KEYDOWN:
                    touches = {K_RIGHT : '_R', K_LEFT : '_L', K_UP : '_U', K_DOWN : '_D', K_RETURN : '_E', K_BACKSPACE : '_B', K_ESCAPE : '_S'}
                    touche = event.key
                    if touche in touches:
                        return touches[touche]
                    return event.unicode
                

if __name__ == "__main__":
    
    interface = GUIsimulation(8, 16) #Créer une interface graphique de 8x8 cases avec 16px de largeur de case
    liste = [[0, 1, 2, 3, 0, 1, 2, 3] for _ in range(8)] #Crée une liste de listes contenant les valeur 0, 1 ,2 et 3
    interface.refresh(liste) #Met à jour l'interface graphique  avec les couleurs contenus dans la matrice de couleur
    print(interface.waitClick()) #Renvoie le numéro de ma case cliquée en indiquant le bouton de souris utilisé. Méthode bloquante.
 