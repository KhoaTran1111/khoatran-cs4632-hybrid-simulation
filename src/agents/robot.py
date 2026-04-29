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

    def is_busy(self):
        """Return True if robot has a goal or is moving"""
        return self.goal is not None or len(self.path) > 0 or self.emergency_goal is not None

    def assign_goal(self, goal, env):
        self.goal = np.array(goal, dtype=float)
        start = tuple(self.position.astype(int))
        goal_tuple = tuple(map(int, goal))
        self.path = astar_search(env, start, goal_tuple)

    def step(self, env):
        if self.emergency_goal is not None:
            return self.step_emergency()

        if not self.path and self.goal is not None:
            # Recompute path if needed
            self.assign_goal(self.goal, env)

        if self.path:
            next_pos = np.array(self.path.pop(0), dtype=float)
            self.position = next_pos
            self.distance_traveled += 1

            # Check if task completed
            if np.linalg.norm(self.position - self.goal) < 0.8:
                self.tasks_completed += 1
                self.goal = None
                self.path = []
                return True  # Task completed this step
        return False

    def emergency_retreat(self, safe_pos, env):
        self.emergency_goal = np.array(safe_pos, dtype=float)
        self.goal = None
        self.path = []
        start = tuple(self.position.astype(int))
        goal_tuple = tuple(map(int, safe_pos))
        self.path = astar_search(env, start, goal_tuple)

    def step_emergency(self):
        if self.path:
            next_pos = np.array(self.path.pop(0), dtype=float)
            self.position = next_pos
            self.distance_traveled += 1
        elif self.emergency_goal is not None and np.linalg.norm(self.position - self.emergency_goal) > 0.5:
            direction = self.emergency_goal - self.position
            norm = np.linalg.norm(direction) + 1e-6
            self.position += (direction / norm) * 1.0