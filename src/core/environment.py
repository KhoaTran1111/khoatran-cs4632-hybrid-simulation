import random

class EnvironmentGrid:
    def __init__(self, width, height, obstacle_ratio=0.1):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self._generate_obstacles(obstacle_ratio)

    def _generate_obstacles(self, ratio):
        for y in range(self.height):
            for x in range(self.width):
                if random.random() < ratio:
                    self.grid[y][x] = 1  # obstacle

    def is_obstructed(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        return self.grid[y][x] == 1

    def neighbors(self, x, y):
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        result = []
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if not self.is_obstructed(nx, ny):
                result.append((nx, ny))
        return result
