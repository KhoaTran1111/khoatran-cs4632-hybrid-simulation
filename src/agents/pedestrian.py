import numpy as np
from algorithms.social_force import social_force

class Pedestrian:
    def __init__(self, ped_id, position, exit_pos):
        self.id = ped_id
        self.position = np.array(position, dtype=float)
        self.exit_pos = exit_pos
        self.evacuated = False

    def step(self, neighbors):
        if self.evacuated:
            return

        force = social_force(self.position, self.exit_pos, neighbors)
        self.position += force * 0.5

        if np.linalg.norm(self.position - self.exit_pos) < 1:
            self.evacuated = True
