import random
from core.environment import EnvironmentGrid

class Task:
    def __init__(self, tid, location):
        self.id = tid
        self.location = location
        self.assigned_to = None
        self.completed = False

class TaskDispatcher:
    def __init__(self, robots, env):
        self.robots = robots
        self.env = env               # ← added
        self.pending_tasks = []
        self.completed_tasks = 0
        self.task_counter = 0

    def generate_order_task(self):
        # Pick random valid location (avoid walls)
        while True:
            x = random.randint(5, self.env.width - 6)
            y = random.randint(5, self.env.height - 6)
            if self.env.is_valid(x, y):
                break
        loc = (x, y)
        task = Task(self.task_counter, loc)
        self.pending_tasks.append(task)
        self.task_counter += 1

    def assign_tasks(self):
        idle_robots = [r for r in self.robots if r.goal is None and r.emergency_goal is None]
        for robot in idle_robots:
            if self.pending_tasks:
                task = self.pending_tasks.pop(0)
                robot.assign_goal(task.location, self.env)   # ← now pass env
                task.assigned_to = robot.id