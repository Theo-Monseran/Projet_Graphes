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
    with open(nom_fichier, 'r') as f:
        for ligne in f:
            if ligne:
                partie = ligne.split(" : ")
                entite = partie[0]
                if (entite != 'X'):
                    position = Position(partie[1].strip("\n").strip("(").strip(")").split(",")[0], 
                                        partie[1].strip("\n").strip("(").strip(")").split(",")[1])
                if entite == 'D':
                    drones.append(position)
                elif entite.isdigit():
                    villages.append(position)
                elif entite == 'E':
                    deplacements.append(position)
    return villages, drones, deplacements


N = 3
nom_fichier = 'data.txt'
villages, drones, deplacements = lire_fichier_graphe(N, nom_fichier)
print(villages[1].x)
print(drones[0].x)
print(drones[0].y)
