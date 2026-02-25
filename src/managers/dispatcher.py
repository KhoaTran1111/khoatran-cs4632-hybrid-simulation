import math

class TaskDispatcher:
    def __init__(self, robots):
        self.task_queue = []
        self.robots = robots

    def add_task(self, task):
        self.task_queue.append(task)

    def assign_tasks(self, environment):
        for task in list(self.task_queue):
            available_robot = self.find_nearest_robot(task.location)

            if available_robot:
                available_robot.assign_task(task, environment)
                self.task_queue.remove(task)

    def find_nearest_robot(self, location):
        best_robot = None
        best_distance = float("inf")

        for robot in self.robots:
            if robot.is_idle():
                dist = math.dist(robot.position, location)
                if dist < best_distance:
                    best_distance = dist
                    best_robot = robot

        return best_robot
