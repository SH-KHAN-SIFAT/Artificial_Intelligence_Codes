import math
import csv
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from collections import defaultdict
from heapq import heapify, heappop, heappush


COORDINATES_FILE = "Coordinates.csv"
DISTANCE_FILE = "distances.csv"

x_points = []               # List of X-Axis Coordinates of all stars
y_points = []               # List of Y-Axis Coordinates of all stars
z_points = []               # List of Z-Axis Coordinates of all stars
stars = []                  # List of the name of all stars


# Heuristic function (Euclidean distance between two points in 3D space) for A* Search Algorithm
def distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


# Dictionary to store the 3D coordinates of each star in the form of (x,y,z) tuples.
coordinates = {}
# Dictionary like object where key = star and its value = list of neighboring stars and their distances
adjacency_list = defaultdict(list)

# Reads the coordinates of each star from the specified CSV file
with open(COORDINATES_FILE, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for star_name, x, y, z in reader:
        stars.append(star_name)                                     # Adding Star names in the list called Stars
        x_points.append(int(x))                                     # Adding X-Axis values of all stars in the list called x_points
        y_points.append(int(y))                                     # Adding Y-Axis values of all stars in the list called y_points
        z_points.append((int(z)))                                   # Adding Z-Axis values of all stars in the list called z_points
        coordinates[star_name] = (int(x), int(y), int(z))           # Storing the 3D coordinates of each star in the form of (x,y,z) tuples in the coordinates dictionary

# Reads the Source star, Destination star & Distance between them from the specified CSV file
with open(DISTANCE_FILE, "r") as file:
    reader = csv.reader(file)
    for source, destination, dist in reader:
        adjacency_list[source].append((destination, int(dist)))    # Creating adjacency List for all stars where key = star & value = neighbour star & distance from source

SOURCE_STAR = "Sun"
DESTINATION_STAR = "HD 219134"

choice = input("Choose algorithm: \n1. Dijkstra \n2. A*\n")        # Algorithm choosing option
if choice == "1":
    algorithm = "Dijkstra"
    DIJKSTRA = True
else:
    algorithm = "A*"
    DIJKSTRA = False

priority_queue = [(0, SOURCE_STAR, None, 0)]        # Priority queue = (Key, Current star, Parent, Distance from source)
visited = set()                                     # Keeping track of visited stars in a set
parent_map = {}                                     # Keeping track of star's parent in parent_map dictionary

while priority_queue:
    # Pop from priority queue will be based on f(n) value....min value will pick first as minheap
    key, current_star, parent, path_distance_from_src = heappop(priority_queue)

    # Skipping the star that appeared more than once
    if current_star in visited:
        continue

    # Current star's parent will be its previous star from which it comes from
    parent_map[current_star] = parent

    # Goal/Destination Star checking , If found return else continue searching
    if current_star == DESTINATION_STAR:
        print("From" + " " + SOURCE_STAR + " " + "to" + " " + DESTINATION_STAR + " , total Distance = " + str(
            path_distance_from_src))
        break

    # Visited star will be added in the set
    visited.add(current_star)

    # Calculating g(n) for each star as it keeps updating in every move
    for neigborstar_name, neigborstar_distance in adjacency_list[current_star]:
        new_path_distance_from_src = path_distance_from_src + neigborstar_distance

        # For Dijkstra , f(n) = g(n) where g(n) = distance between two stars that keeps updating like g(n) update like
        # g(n) = g(n)+current star to next star distance
        if DIJKSTRA:
            heappush(priority_queue,
                     (new_path_distance_from_src, neigborstar_name, current_star, new_path_distance_from_src))

        # For A* f(n) = g(n) + h(n) , where g(n) = distance between two stars that keeps updating like
        # g(n) = g(n)+current to next star distance
        else:
            heappush(priority_queue, (
            new_path_distance_from_src + distance(*coordinates[neigborstar_name], *coordinates[DESTINATION_STAR]),
            neigborstar_name, current_star, new_path_distance_from_src))

# Path printing from source to destination
if DESTINATION_STAR not in parent_map:
    print("Cannot reach destination")

# Finding the path by backtracking & printing the path from source to destination
else:
    path = []                                           # List of stars that are on the path from source to destination
    current_star = DESTINATION_STAR
    while current_star != SOURCE_STAR:
        path.append(current_star)
        current_star = parent_map[current_star]
    path.append(SOURCE_STAR)
    print(f"{algorithm} Path: {' -> '.join(reversed(path))}")

# for 3D Drawing in 3D Plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot stars
ax.scatter(x_points, y_points, z_points, c='black', marker='*', s=100)

# Plot path from source to destination
if DESTINATION_STAR in parent_map:
    path = []
    current_star = DESTINATION_STAR
    while current_star != SOURCE_STAR:
        path.append(current_star)
        current_star = parent_map[current_star]
    path.append(SOURCE_STAR)
    path_x = [x_points[stars.index(star)] for star in path]
    path_y = [y_points[stars.index(star)] for star in path]
    path_z = [z_points[stars.index(star)] for star in path]
    ax.plot(path_x, path_y, path_z, c='red', linestyle='-')

# Set labels
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.set_zlabel('Z Coordinate')
ax.set_title('3D Coordinates of Stars')

plt.show()

