import numpy as np

def social_force(position, goal, neighbors, strength=0.5):
    force = np.array(goal) - np.array(position)
    force = force / (np.linalg.norm(force) + 1e-5)

    for n in neighbors:
        diff = np.array(position) - np.array(n)
        dist = np.linalg.norm(diff)
        if dist < 2 and dist > 0:
            force += strength * (diff / dist)

    return force
