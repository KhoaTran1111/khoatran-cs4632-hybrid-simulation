import random

# src/core/environment.py

class EnvironmentGrid:
    def __init__(self, width, height, walls=None):
        self.width = width
        self.height = height
        self.walls = walls or []  # list of [x1,y1,x2,y2] rectangles for obstacles/shelves

    def is_valid(self, x, y):
        """Check if position (x,y) is inside grid and not inside any wall."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        for wx1, wy1, wx2, wy2 in self.walls:
            if wx1 <= x <= wx2 and wy1 <= y <= wy2:
                return False
        return True

    def neighbors(self, x, y):
        """Return list of valid adjacent positions (4-directional)."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
        result = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny):
                result.append((nx, ny))
        return result