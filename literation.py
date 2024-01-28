import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class NLateration:
    def __init__(self, emitters, distances):
        self.emitters = emitters
        self.distances = distances
        self.initial_position = np.zeros(3)
        self.result = None
        self.receiver_position = None

    def objective_function(self, coordinates):
        return np.sum([(np.linalg.norm(coordinates - emitter) - distance)**2 for emitter, distance in zip(self.emitters, self.distances)])

    def run_NLateration(self):
        print("Script is running!")
        self.result = minimize(self.objective_function, self.initial_position)
        print("Script reached here")
        self.receiver_position = self.result.x
        print("Estimated Receiver Position:", self.receiver_position)

    def visualize_NLateration(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(self.emitters[:, 0], self.emitters[:, 1], self.emitters[:, 2], c='r', marker='o', label='Emitters')

        for emitter, distance in zip(self.emitters, self.distances):
            circle_center = self.receiver_position + (emitter - self.receiver_position) / np.linalg.norm(emitter - self.receiver_position) * distance

            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            x = circle_center[0] + distance * np.outer(np.cos(u), np.sin(v))
            y = circle_center[1] + distance * np.outer(np.sin(u), np.sin(v))
            z = circle_center[2] + distance * np.outer(np.ones(np.size(u)), np.cos(v))
            ax.plot_surface(x, y, z, color='gray', alpha=0.3)

        ax.scatter(self.receiver_position[0], self.receiver_position[1], self.receiver_position[2], c='b', marker='x', label='Estimated Receiver')
        ax.text(self.receiver_position[0], self.receiver_position[1], self.receiver_position[2],
                f'({self.receiver_position[0]:.2f}, {self.receiver_position[1]:.2f}, {self.receiver_position[2]:.2f})', color='b')

        plt.legend()
        plt.show()


#given data
emitters_data = np.array([[0.5, 0.5, 0.5], [4, 0, 0], [4, 5, 5], [3, 3, 3]])
distances_data = np.array([3, 2, 4.2, 2.5])

n_lateration = NLateration(emitters_data, distances_data)

n_lateration.run_NLateration()

n_lateration.visualize_NLateration()
