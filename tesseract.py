import matplotlib.pyplot as plt
import math

def levenshtein(s1, s2):
    # Calculate the Levenshtein distance between two strings
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
 
    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)
 
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
           insertions = previous_row[j + 1] + 1
           deletions = current_row[j] + 1
           substitutions = previous_row[j] + (c1 != c2)
           current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
 
    return previous_row[-1]


def posFromRelDist(dist1, x1, y1, dist2, x2, y2) -> (int, int):
    # Get the position of a point given the relative distances to two other points
    try:
        # Calculate the distance between the two points
        dist = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
        # Calculate the angle between the two points
        angle = math.atan2(y2 - y1, x2 - x1)
        # Calculate the angle between the new point and the first point
        angle1 = math.acos((dist1**2 + dist**2 - dist2**2) / (2 * dist1 * dist))
        # Calculate the new point's x and y coordinates
        x = x1 + dist1 * math.cos(angle + angle1)
        y = y1 + dist1 * math.sin(angle + angle1)
        return (x, y)
    except Exception as e:
        # If the math fails, return (0, 0)
        print(f"Error: point at (0, 0) {e}")
        return (0, 0)


def getNthNearest(distances, n, i):
    dists = [distances[i][k] for k in range(len(distances[i])) if k != i]
    # Sort the distances
    dists.sort()
    # Get the nth nearest point
    for j in range(len(distances[i])):
        if distances[i][j] == dists[n - 1]:
            return j


def shortestEdgePairBetweenTwoSubgraphs(distances, a, b):
    shortest_sum = float("inf")
    cross_edges = []
    for i in a:
        cross_edge_row = []
        for j in b:
            cross_edge_row.append((distances[i][j], i, j))
        cross_edge_row.sort(key = lambda x: x[0])
        cross_edges.append(cross_edge_row)
    # Find the smallest sum of the first two edges
    smallest_edges = []
    shortest_sum = float("inf")
    for i in range(len(cross_edges)):
        if cross_edges[i][0][0] + cross_edges[i][1][0] < shortest_sum:
            shortest_sum = cross_edges[i][0][0] + cross_edges[i][1][0]
            smallest_edges = [(cross_edges[i][0][1], cross_edges[i][0][2]), (cross_edges[i][1][1], cross_edges[i][1][2])]
    return smallest_edges


# Open tests/long_http_1000 and load each file into an input string
inputs = []
#for i in range(200):
#    with open("tests/long_http_200/" + str(i) + ".txt", "r") as f:
for i in range(11):
    with open("tests/simple/" + str(i) + ".txt", "r") as f:
        inputs.append(f.read())



# Build a distance matrix between each input
distances = []
for i in range(len(inputs)):
    distances.append([])
    for j in range(len(inputs)):
        distances[i].append(levenshtein(inputs[i], inputs[j]))


# Start with the first point at (0, 0)
positions = [() for _ in range(len(inputs))]
positions[0] = (0, 0)

# Find the nearest point to the first point
nearest_0 = getNthNearest(distances, 1, 0)
positions[nearest_0] = (distances[0][nearest_0], 0)

print(positions)
while any([p == () for p in positions]):
    # Find the point that has the lowest sum of 2 distances to points that have already been placed
    shortestEdgePair = shortestEdgePairBetweenTwoSubgraphs(distances, [j for j in range(len(inputs)) if positions[j] == ()], [j for j in range(len(inputs)) if positions[j] != ()])
    print(shortestEdgePair)
    new_i = shortestEdgePair[0][0]
    a_i = shortestEdgePair[0][1]
    b_i = shortestEdgePair[1][1]
    new = positions[new_i]
    a = positions[a_i]
    b = positions[b_i]
    positions[shortestEdgePair[0][0]] = posFromRelDist(distances[new_i][a_i], a[0], a[1], distances[new_i][b_i], b[0], b[1])


# Plot the points
x = [p[0] for p in positions]
y = [p[1] for p in positions]
plt.scatter(x, y)
# Make the plot square
plt.gca().set_aspect('equal', adjustable='box')
plt.show()