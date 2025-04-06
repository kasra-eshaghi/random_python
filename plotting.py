import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Define cube corners (origin at 0,0,0)
origin = np.array([0, 0, 0])
size = 1  # Cube side length

# 8 corners of the cube
points = np.array([
    origin,
    origin + [size, 0, 0],
    origin + [size, size, 0],
    origin + [0, size, 0],
    origin + [0, 0, size],
    origin + [size, 0, size],
    origin + [size, size, size],
    origin + [0, size, size]
])

# Define the 6 faces as lists of vertex indices
faces = [
    [points[0], points[1], points[2], points[3]],  # bottom
    [points[4], points[5], points[6], points[7]],  # top
    [points[0], points[1], points[5], points[4]],  # front
    [points[2], points[3], points[7], points[6]],  # back
    [points[1], points[2], points[6], points[5]],  # right
    [points[0], points[3], points[7], points[4]]   # left
]

cube = Poly3DCollection(faces, facecolors='lightblue', linewidths=1, edgecolors='black', alpha=0.8)
ax.add_collection3d(cube)

ax.set_xlim([0, 2])
ax.set_ylim([0, 2])
ax.set_zlim([0, 2])
ax.set_box_aspect([1, 1, 1])  # Equal aspect ratio
plt.show()
