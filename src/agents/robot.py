from algorithms.pathfinding import astar_search

class Robot:
    def __init__(self, robot_id, position):
        self.id = robot_id
        self.position = position
        self.task_queue = []
        self.path = []
        self.current_task = None
        self.distance_traveled = 0

    def is_idle(self):
        return self.current_task is None and not self.task_queue

    def assign_task(self, task, env):
        self.task_queue.append(task)
        if not self.current_task:
            self.start_next_task(env)

    def start_next_task(self, env):
        if self.task_queue:
            self.current_task = self.task_queue.pop(0)
            self.path = astar_search(env, self.position, self.current_task.location)

    def step(self, env, emergency_mode=False):
        if emergency_mode:
            return  # robots stop during emergency

        if self.path:
            next_pos = self.path.pop(0)
            self.distance_traveled += 1
            self.position = next_pos

        elif self.current_task:
            print(f"Robot {self.id} completed Task {self.current_task.task_id}")
            self.current_task.completed = True
            self.current_task = None
            self.start_next_task(env)
