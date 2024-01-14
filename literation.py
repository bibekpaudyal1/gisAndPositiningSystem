import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def objective_function(coordinates, *args):
    emitters, distances = args
    return np.sum([(np.linalg.norm(coordinates - emitter) - distance)**2 for emitter, distance in zip(emitters, distances)])

# Given data
emitters = np.array([[0.5, 0.5, 0.5], [4, 0, 0], [4, 5, 5], [3, 3, 3]])
distances = np.array([3, 2, 4.2, 2.5])

# Initial guess for receiver position
initial_position = np.zeros(3)

print("Script is running!")

result = minimize(objective_function, initial_position, args=(emitters, distances))
print("Script reached here")
# Estimated receiver position
receiver_position = result.x
print("Estimated Receiver Position:", receiver_position)

# Visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(emitters[:, 0], emitters[:, 1], emitters[:, 2], c='r', marker='o', label='Emitters')


for emitter, distance in zip(emitters, distances):
    # Calculate the corrected position based on the estimated receiver position
    circle_center = receiver_position + (emitter - receiver_position) / np.linalg.norm(emitter - receiver_position) * distance

    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = circle_center[0] + distance * np.outer(np.cos(u), np.sin(v))
    y = circle_center[1] + distance * np.outer(np.sin(u), np.sin(v))
    z = circle_center[2] + distance * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='gray', alpha=0.3)

# Plot estimated receiver position
ax.scatter(receiver_position[0], receiver_position[1], receiver_position[2], c='b', marker='x', label='Estimated Receiver')

# Annotate the estimated receiver position with coordinates
ax.text(receiver_position[0], receiver_position[1], receiver_position[2],
        f'({receiver_position[0]:.2f}, {receiver_position[1]:.2f}, {receiver_position[2]:.2f})', color='b')

plt.legend()
plt.show()
