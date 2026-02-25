import random
from utils.metrics import Metrics

class SimulationEngine:
    def __init__(self, env, robots, pedestrians, max_steps=100):
        self.env = env
        self.robots = robots
        self.pedestrians = pedestrians
        self.time = 0
        self.max_steps = max_steps
        self.emergency_mode = False
        self.metrics = Metrics()

    def trigger_emergency(self):
        print("EMERGENCY TRIGGERED")
        self.emergency_mode = True

    def step(self):
        self.time += 1

        # Robots move normally unless emergency
        if not self.emergency_mode:
            for r in self.robots:
                r.step()

        # Pedestrians evacuate during emergency
        if self.emergency_mode:
            for p in self.pedestrians:
                neighbors = [other.position for other in self.pedestrians if other != p]
                p.step(neighbors)

        # Check evacuation complete
        if self.emergency_mode:
            if all(p.evacuated for p in self.pedestrians):
                self.metrics.record_evacuation(self.time)
                return False

        if self.time >= self.max_steps:
            return False

        return True

    def run(self):
        while self.step():
            if self.time == 30:
                self.trigger_emergency()

        self.metrics.record_robot(self.robots)
        self.metrics.report()
