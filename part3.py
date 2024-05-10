import numpy as np

def distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

#def parcours_optimal(village, drones, deplacements):
#    visited = np.zeros(len[village])
#    pass
    