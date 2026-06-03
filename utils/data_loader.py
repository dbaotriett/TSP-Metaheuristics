import math

def readTspEuc2d(filepath):
    coordinates = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    startIndex = 0
    for i, line in enumerate(lines):
        if line.startswith('NODE_COORD_SECTION'):
            startIndex = i + 1
            break

    for line in lines[startIndex:]:
        if line.startswith('EOF') or line.startswith('DISPLAY_DATA_SECTION'):
            break
        parts = line.strip().split()
        if len(parts) >= 3:
            coordinates.append((float(parts[1]), float(parts[2])))

    n = len(coordinates)
    dist = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            dx = coordinates[i][0] - coordinates[j][0]
            dy = coordinates[i][1] - coordinates[j][1]
            dij = int(math.sqrt(dx*dx + dy*dy) + 0.5)
            dist[i][j] = dist[j][i] = dij

    return dist, n