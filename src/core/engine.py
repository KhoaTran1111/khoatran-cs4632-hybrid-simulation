import random
from utils.metrics import Metrics
from managers.dispatcher import TaskDispatcher
from managers.order_generator import OrderGenerator

class SimulationEngine:
    def __init__(self, env, robots, pedestrians, inventory, max_steps=200):
        self.env = env
        self.robots = robots
        self.pedestrians = pedestrians
        self.inventory = inventory
        self.dispatcher = TaskDispatcher(robots)
        self.order_generator = OrderGenerator(env, inventory)

        self.time = 0
        self.max_steps = max_steps
        self.emergency_mode = False
        self.metrics = Metrics()

    def trigger_emergency(self):
        print("EMERGENCY TRIGGERED")
        self.emergency_mode = True
        self.inventory.set_emergency_mode(True)

    def step(self):
        self.time += 1

        # Generate random orders in normal mode
        if not self.emergency_mode and random.random() < 0.2:
            task = self.order_generator.generate_order()
            self.dispatcher.add_task(task)

        # Assign tasks
        if not self.emergency_mode:
            self.dispatcher.assign_tasks(self.env)

        # Move robots
        for r in self.robots:
            r.step(self.env, self.emergency_mode)

        # Pedestrian evacuation
        if self.emergency_mode:
            for p in self.pedestrians:
                neighbors = [other.position for other in self.pedestrians if other != p]
                p.step(neighbors)

            if all(p.evacuated for p in self.pedestrians):
                self.metrics.record_evacuation(self.time)
                return False

        if self.time == 80:
            self.trigger_emergency()

        if self.time >= self.max_steps:
            return False

        return True

    def run(self):
        while self.step():
            pass

        self.metrics.record_robot(self.robots)
        self.metrics.report()