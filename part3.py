import numpy as np
from part2 import *


def distance(p1, p2):
    return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


# return list of villages from nearest to drones to furthest
# (0 is the one the drone is currently on)
def get_nearest(villages, drone, deplacements):
    # TODO
    pass


def tsp_glouton(villages, drones, deplacements, num_tournees=1):

    i = 0
    for tournee in num_tournees:
        visited = []
        damage = [0 for i in range(len(villages))]
        for drone in drones:
            visited.append([drone.x, drone.y])
        while len(visited) < len(villages):
            for drone in drones:
                nearest_villages = get_nearest(villages, drone, deplacements)
                for village in nearest_villages:
                    if village not in visited:
                        drone.x = village.x
                        drone.y = village.y
            for v in range(len(villages)):
                if villages[v] not in visited:
                    damage[v] += 1
            i += 1
    return i, damage
