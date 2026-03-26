import numpy as np

class SocialForceModel:
    def __init__(self, a=10.0, b=0.5, strength_rep=2.0, strength_wall=5.0):
        self.a = a  # relaxation time
        self.b = b  # repulsive distance scale
        self.strength_rep = strength_rep
        self.strength_wall = strength_wall

    def compute_force(self, pos, goal, neighbors, walls, velocity=np.array([0.,0.])):
        # Desired direction & velocity
        direction = goal - pos
        dist_to_goal = np.linalg.norm(direction)
        if dist_to_goal > 1e-6:
            desired_vel = (direction / dist_to_goal) * 1.2  # max desired speed
        else:
            desired_vel = np.zeros(2)

        driving_force = (desired_vel - velocity) / self.a

        # Pedestrian repulsion
        repulsion = np.zeros(2)
        for n_pos in neighbors:
            diff = pos - n_pos
            d = np.linalg.norm(diff)
            if 0.1 < d < 3.0:
                repulsion += self.strength_rep * np.exp(-d / self.b) * (diff / d)

        # Wall/obstacle repulsion (simple box check)
        wall_rep = np.zeros(2)
        for wx1, wy1, wx2, wy2 in walls:
            # Approximate nearest point on wall rectangle (simplified)
            closest_x = np.clip(pos[0], wx1, wx2)
            closest_y = np.clip(pos[1], wy1, wy2)
            diff = pos - np.array([closest_x, closest_y])
            d_wall = np.linalg.norm(diff)
            if d_wall < 2.0 and d_wall > 0.01:
                wall_rep += self.strength_wall * (1 / d_wall) * (diff / d_wall)

        total_force = driving_force + repulsion + wall_rep
        return total_force