import random
from agents.robot import Robot
from core.environment import EnvironmentGrid

class Task:
    def __init__(self, tid, location):
        self.id = tid
        self.location = location
        self.assigned_to = None
        self.completed = False

class TaskDispatcher:
    def __init__(self, robots, env: EnvironmentGrid):
        self.robots = robots
        self.env = env
        self.pending_tasks = []
        self.completed_tasks = 0
        self.task_counter = 0

    def generate_order_task(self):
        """Generate a new pick task at a random valid shelf location"""
        attempts = 0
        while attempts < 20:
            x = random.randint(5, self.env.width - 6)
            y = random.randint(5, self.env.height - 6)
            if self.env.is_valid(x, y):
                task = Task(self.task_counter, (x, y))
                self.pending_tasks.append(task)
                self.task_counter += 1
                return
            attempts += 1

    def assign_tasks(self):
        """Proactively assign pending tasks to ALL idle robots"""
        idle_robots = [r for r in self.robots 
                      if r.goal is None and r.emergency_goal is None and not r.is_busy()]
        
        for robot in idle_robots:
            if not self.pending_tasks:
                break
            task = self.pending_tasks.pop(0)
            robot.assign_goal(task.location, self.env)
            task.assigned_to = robot.id

    def update_completed_tasks(self):
        """Check if any assigned tasks are completed"""
        for task in self.pending_tasks[:]:
            pass