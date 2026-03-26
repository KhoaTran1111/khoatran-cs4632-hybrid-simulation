import numpy as np
from algorithms.pathfinding import astar_search

class Robot:
    def __init__(self, rid, position):
        self.id = rid
        self.position = np.array(position, dtype=float)
        self.goal = None
        self.path = []
        self.distance_traveled = 0
        self.tasks_completed = 0
        self.emergency_goal = None

    def assign_goal(self, goal, env):
        self.goal = goal
        self.path = astar_search(env, tuple(self.position.astype(int)), goal)
        if not self.path:
            self.path = []  # no path

    def step(self, env):
        if self.emergency_goal:
            return  # emergency overrides
        if not self.path and self.goal:
            self.path = astar_search(env, tuple(self.position.astype(int)), tuple(self.goal))
        if self.path:
            next_pos = np.array(self.path.pop(0), dtype=float)
            self.position = next_pos
            self.distance_traveled += 1
            # Check task completion
            if np.linalg.norm(self.position - self.goal) < 0.5:
                self.tasks_completed += 1
                self.goal = None
                self.path = []

    def emergency_retreat(self, safe_pos, env):
        self.emergency_goal = np.array(safe_pos)
        self.goal = None
        self.path = []  # clear normal path

    def step_emergency(self):
        if self.emergency_goal is not None and np.linalg.norm(self.position - self.emergency_goal) > 0.5:
            direction = self.emergency_goal - self.position
            direction /= np.linalg.norm(direction) + 1e-6
            self.position += direction * 1.0  # fast retreat