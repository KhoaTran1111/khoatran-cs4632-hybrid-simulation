import numpy as np

class Pedestrian:
    def __init__(self, pid, position, exit_pos):
        self.id = pid
        self.position = np.array(position, dtype=float)
        self.exit_pos = np.array(exit_pos, dtype=float)
        self.evacuated = False
        self.velocity = np.zeros(2, dtype=float)

    def step_evacuate(self, neighbors, sf_model, walls):
        if self.evacuated:
            return
        force = sf_model.compute_force(self.position, self.exit_pos, neighbors, walls, self.velocity)
        accel = force  # simplified
        self.velocity += accel * 0.1  # dt=0.1 internal
        self.velocity = np.clip(self.velocity, -1.5, 1.5)
        self.position += self.velocity * 0.1
        if np.linalg.norm(self.position - self.exit_pos) < 1.0:
            self.evacuated = True

    def step_normal(self, neighbors, sf_model, walls):
        # Placeholder: random wander or slow movement
        pass