def lire_fichier_graphe(N, nom_fichier):
    graphe = {'villages': [], 'drones': [], 'deplacements': []}
    with open(nom_fichier, 'r') as f:
        for ligne in f:
            if ligne:
                partie = ligne.split(" : ")
                entite = partie[0]
                if (entite != 'X'):
                    position = [int(x) for x in partie[1].strip("\n").strip("(").strip(")").split(",")]
                if entite == 'D':
                    graphe['drones'].append(position)
                elif entite.isdigit():
                    graphe['villages'].append(position)
                elif entite == 'E':
                    graphe['deplacements'].append(position)
    return graphe

N = 3
nom_fichier = 'data.txt'
graphe = lire_fichier_graphe(N, nom_fichier)
print(graphe)
