import math
import csv
import random
from collections import defaultdict
from heapq import heapify, heappop, heappush

COORDINATES_FILE = "Coordinates.csv"
DISTANCE_FILE = "distances.csv"

coordinates = {}
adjacency_list = defaultdict(list)

with open(COORDINATES_FILE, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for star_name, x, y, z in reader:
        coordinates[star_name] = (int(x), int(y), int(z))

with open(DISTANCE_FILE, "r") as file:
    reader = csv.reader(file)
    for source, destination, dist in reader:
        adjacency_list[source].append((destination, int(dist)))

SOURCE_STAR = "TRAPPIST-1"
DESTINATION_STAR = "55 Cancri"

choice = int(input("Enter 1 for Dijkstra's algorithm or 2 for A* algorithm: "))

if choice == 1:
    # Dijkstra's algorithm
    priority_queue = [(0, SOURCE_STAR, None)]
    visited = set()
    parent_map = {}
    distance_from_src = {star_name: float('inf') for star_name in coordinates.keys()}
    distance_from_src[SOURCE_STAR] = 0

    while priority_queue:
        path_distance_from_src, current_star, parent_star = heappop(priority_queue)
        if current_star in visited:
            continue
        if current_star == DESTINATION_STAR:
            print("Reached " + DESTINATION_STAR + " Distance = " + str(path_distance_from_src))
            break
        visited.add(current_star)
        parent_map[current_star] = parent_star
        for neighborstar_name, neighborstar_distance in adjacency_list[current_star]:
            new_path_distance_from_src = path_distance_from_src + neighborstar_distance
            if new_path_distance_from_src < distance_from_src[neighborstar_name]:
                distance_from_src[neighborstar_name] = new_path_distance_from_src
                heappush(priority_queue, (new_path_distance_from_src, neighborstar_name, current_star))

elif choice == 2:
    # A* algorithm
    def distance(x1, y1, z1, x2, y2, z2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

    priority_queue = [(0, SOURCE_STAR)]
    visited = set()
    parent_map = {}
    distance_from_src = {star_name: float('inf') for star_name in coordinates.keys()}
    distance_from_src[SOURCE_STAR] = 0

    while priority_queue:
        path_distance_from_src, current_star = heappop(priority_queue)
        if current_star in visited:
            continue
        if current_star == DESTINATION_STAR:
            print("Reached " + DESTINATION_STAR + " Distance = " + str(distance_from_src[DESTINATION_STAR]))
            break
        visited.add(current_star)
        for neighbor_star, neighbor_distance in adjacency_list[current_star]:
            new_path_distance_from_src = distance_from_src[current_star] + neighbor_distance
            if new_path_distance_from_src < distance_from_src[neighbor_star]:
                distance_from_src[neighbor_star] = new_path_distance_from_src
                priority = new_path_distance_from_src + distance(*coordinates[neighbor_star], *coordinates[DESTINATION_STAR])
                heappush(priority_queue, (priority, neighbor_star))
                parent_map[neighbor_star] = current_star
