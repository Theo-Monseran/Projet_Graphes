import numpy as np
import matplotlib.pyplot as plt
import re


class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @staticmethod
    def string_to_pos(string):
        x_y = string[1:len(string)-2].split(",")
        return Position(int(x_y[0]), int(x_y[1]))


def lire_fichier_graphe(N, nom_fichier):
    villages = []
    drones = []
    deplacements = []
    obstacles = []
    with open(nom_fichier, 'r') as f:
        for ligne in f:
            if ligne:
                partie = ligne.split(" : ")
                entite = partie[0]
                if (entite == 'X'):
                    matches = re.findall(r'\((\d+),(\d+)\)', ligne)

                    # Extraire et stocker les coordonnées de la première position
                    x1, y1 = matches[0]
                    position1 = Position(x1, y1)

                    # Extraire et stocker les coordonnées de la deuxième position
                    x2, y2 = matches[1]
                    position2 = Position(x2, y2)
                    
                    obstacles.append([position1, position2])

                if (entite != 'X'):
                    position = Position(partie[1].strip("\n").strip("(").strip(")").split(",")[0], 
                                        partie[1].strip("\n").strip("(").strip(")").split(",")[1])
                if entite == 'D':
                    drones.append(position)
                elif entite.isdigit():
                    villages.append(position)
                elif entite == 'E':
                    deplacements.append(position)
    return villages, drones, deplacements, obstacles



def afficher_monde_terminal(villages, drones, obstacles, deplacements):
    # Trouver les limites du monde
    max_x = max(int(village.x) for village in villages)
    max_y = max(int(village.y) for village in villages)

    # Ajouter les coordonnées des obstacles à considérer pour les limites du monde
    for obstacle in obstacles:
        max_x = max(max_x, int(obstacle[0].x), int(obstacle[1].x))
        max_y = max(max_y, int(obstacle[0].y), int(obstacle[1].y))

    # Créer une matrice représentant le monde avec des espaces vides
    monde = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Dictionnaire pour suivre les villages déjà placés
    villages_places = {}

    # Placer les villages sur la matrice avec leur numéro
    for i, village in enumerate(villages):
        x, y = int(village.x), int(village.y)
        if (x, y) in villages_places:
            monde[y][x] = villages_places[(x, y)]
        else:
            village_str = f'V{i}'
            monde[y][x:x+len(village_str)] = village_str
            villages_places[(x, y)] = village_str

    # Placer les drones sur la matrice
    for drone in drones:
        x, y = int(drone.x), int(drone.y)
        if (x, y) in villages_places:
            # Déplacer le drone à une position adjacente s'il est sur un village
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x <= max_x and 0 <= new_y <= max_y and (new_x, new_y) not in villages_places:
                    monde[new_y][new_x] = 'D'
                    break
        else:
            monde[y][x] = 'D'

    # Placer les obstacles sur la matrice sous forme de rectangle
    for obstacle in obstacles:
        inf_gauche, sup_droit = obstacle
        for y in range(int(inf_gauche.y), int(sup_droit.y) + 1):
            for x in range(int(inf_gauche.x), int(sup_droit.x) + 1):
                monde[y][x] = 'X'

    # Placer les déplacements sur la matrice
    for deplacement in deplacements:
        monde[int(deplacement.y)][int(deplacement.x)] = 'E'

    # Afficher la matrice
    for ligne in monde:
        print(''.join(ligne))




def afficher_monde(villages, drones, obstacles, deplacements):
    # Trouver les limites du monde
    max_x = max(int(village.x) for village in villages)
    max_y = max(int(village.y) for village in villages)

    # Ajouter les coordonnées des obstacles à considérer pour les limites du monde
    for obstacle in obstacles:
        max_x = max(max_x, int(obstacle[0].x), int(obstacle[1].x))
        max_y = max(max_y, int(obstacle[0].y), int(obstacle[1].y))

    # Créer une matrice représentant le monde avec des espaces vides
    monde = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Placer les villages sur la matrice
    for i, village in enumerate(villages):
        monde[int(village.y)][int(village.x)] = i + 1  # Utiliser les numéros des villages

    # Placer les drones sur la matrice
    for drone in drones:
        monde[int(drone.y)][int(drone.x)] = 'D'

    # Placer les obstacles sur la matrice sous forme de rectangle
    for obstacle in obstacles:
        inf_gauche, sup_droit = obstacle
        for y in range(int(inf_gauche.y), int(sup_droit.y) + 1):
            for x in range(int(inf_gauche.x), int(sup_droit.x) + 1):
                monde[y][x] = 'X'

    # Créer l'image du monde
    cmap = {' ': 0, 'D': 1, 'X': 2, 'E': 3}  # Supprimer les villages du dictionnaire cmap
    image = np.array([[cmap[cell] if cell in cmap else 4 for cell in row] for row in monde])  # Utiliser 4 pour les villages

    # Afficher l'image
    plt.imshow(image, cmap='terrain', interpolation='nearest')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xticks(np.arange(0, max_x + 1, step=1))
    plt.yticks(np.arange(0, max_y + 1, step=1))
    plt.grid(color='black', linewidth=0.5)
    plt.title('Visualisation du monde')

    # Ajouter l'explication des couleurs
    plt.text(max_x + 1, max_y, 'Explication des couleurs:', fontsize=10, ha='left')
    plt.text(max_x + 1, max_y + 0.5, 'Blanche: Village', fontsize=10, ha='left')
    plt.text(max_x + 1, max_y + 1, 'Vert: Drone', fontsize=10, ha='left')
    plt.text(max_x + 1, max_y + 1.5, 'Bleu: Déplacement', fontsize=10, ha='left')
    plt.text(max_x + 1, max_y + 2, 'Jaune: Obstacle', fontsize=10, ha='left')

    plt.show()

# ------------------------------------- test ----------------------------------------------------------------------------


N = 3
nom_fichier = 'data.txt'
villages, drones, deplacements, obstacles = lire_fichier_graphe(N, nom_fichier)

for i in range(len(villages)):
    print(villages[i].x, "  ", villages[i].y)

for i in range(len(drones)):
    print(drones[i].x, "  ", drones[i].y)  

for i in range(len(deplacements)):
    print(deplacements[i].x, "  ", deplacements[i].y)

for i in range(len(obstacles)):
    print(obstacles[i][0].x, " ", obstacles[i][0].y, ";", obstacles[i][1].x, "  ", obstacles[i][1].y)


afficher_monde_terminal(villages, drones, obstacles, deplacements)

afficher_monde(villages, drones, obstacles, deplacements)


