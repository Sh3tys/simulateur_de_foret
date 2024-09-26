#----- Bibliothèques -----
import matrice  # On importe le fichier matrice.py comme bibliothèque
import time
import random

#----- Fonctions -----

#----- Programme principal -----
pourcen_foret = int(input("Densité de la forêt (0-100):")) / 100
pourcen_nu = 1 - pourcen_foret

# Ci-dessous, un exemple pour représenter facilement une matrice avec 4 couleurs différentes pour les cellules
ma_foret = matrice.GUIsimulation(50, 16)  # Créer une interface graphique de 8x8 cases avec 16px de largeur de case
liste = []
for i in range(50):
    liste.append([])
    for j in range(50):
        # Choisir entre 0 et 1 avec une probabilité de 0.2 pour 1 et 0.8 pour 0
        etat = random.choices([0, 1], weights=[pourcen_nu, pourcen_foret])[0]
        liste[i].append(etat)
# Création d'une liste qui contient huit listes chacune composée des nombres 0 à 3

ma_foret.refresh(liste)  # Met à jour l'interface graphique avec les couleurs contenus dans la matrice de couleur

time.sleep(3)  # On attend trois secondes

# On modifie le contenu de la liste
clic = list(ma_foret.waitClick())  # Fonction bloquante qui attend qu'on clique dans l'IHM et qui renvoie une liste constituée de la colonne, de la ligne et du bouton de souris)
print(type(clic))
print(clic)

x = clic[0]
y = clic[1]
liste[y][x] = 2
ma_foret.refresh(liste)  # Met à jour l'interface graphique avec les couleurs contenus dans la matrice de couleur

# liste[i][j] == 0 ou a la fin
feu = [(x, y)]  # Liste des cases en feu
while feu:
    # Vérifier les cases adjacentes et propager le feu
    feu_propage = []  # Liste pour stocker les nouvelles cases en feu
    for i, j in feu:
        liste[j][i] = 3

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = i + dx, j + dy
            if 0 <= nx < 50 and 0 <= ny < 50 and liste[ny][nx] == 1:
                liste[ny][nx] = 2
                feu_propage.append((nx, ny))
    feu = feu_propage

    ma_foret.refresh(liste)
    time.sleep(0.1)
