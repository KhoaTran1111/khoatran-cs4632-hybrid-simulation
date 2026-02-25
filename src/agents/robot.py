from algorithms.pathfinding import astar_search

class Robot:
    def __init__(self, robot_id, position):
        self.id = robot_id
        self.position = position
        self.goal = None
        self.path = []
        self.distance_traveled = 0

    def assign_goal(self, goal, env):
        self.goal = goal
        self.path = astar_search(env, self.position, goal)

    def step(self):
        if self.path:
            next_pos = self.path.pop(0)
            self.distance_traveled += 1
            self.position = next_pos
