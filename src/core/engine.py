import numpy as np
import random
from agents.robot import Robot
from agents.pedestrian import Pedestrian
from algorithms.pathfinding import astar_search
from algorithms.social_force import SocialForceModel
from managers.task_dispatcher import TaskDispatcher
from utils.metrics import MetricsCollector
from core.environment import EnvironmentGrid

class SimulationEngine:
    def __init__(self, config):
        self.config = config
        self.time = 0
        self.max_steps = config['simulation']['max_steps']
        self.emergency_mode = False
        self.trigger_step = config['emergency']['trigger_step']

        # Environment
        self.grid_w = config['simulation']['grid_width']
        self.grid_h = config['simulation']['grid_height']
        self.walls = config['warehouse']['shelves']
        self.exits = config['warehouse']['exits']

        # Create environment object
        self.env = EnvironmentGrid(self.grid_w, self.grid_h, self.walls)

        # Agents
        self.robots = []
        self.pedestrians = []
        self._init_agents()

        # Models & managers
        self.sf_model = SocialForceModel()
        self.dispatcher = TaskDispatcher(self.robots, self.env)

        # Metrics
        self.metrics = MetricsCollector(config['metrics']['output_dir'], self.time)

        random.seed(config['simulation']['random_seed'])
        np.random.seed(config['simulation']['random_seed'])

    def _init_agents(self):
        for i in range(self.config['agents']['num_robots']):
            pos = [random.randint(2, self.grid_w-3), random.randint(2, self.grid_h-3)]
            self.robots.append(Robot(i, pos))

        for i in range(self.config['agents']['num_pedestrians']):
            pos = [random.randint(5, self.grid_w-6), random.randint(5, self.grid_h-6)]
            exit_pos = random.choice(self.exits)
            self.pedestrians.append(Pedestrian(i, pos, exit_pos))

    def trigger_emergency(self):
        print(f"EMERGENCY TRIGGERED at step {self.time}")
        self.emergency_mode = True
        for r in self.robots:
            r.emergency_retreat(self._get_nearest_safe_zone(r.position), self.env)

    def _get_nearest_safe_zone(self, pos):
        safe = self.config['emergency']['safe_zones']
        dists = [np.linalg.norm(np.array(pos) - np.array(s)) for s in safe]
        return safe[np.argmin(dists)]

    def step(self):
        self.time += 1

        # Generate new orders (Poisson)
        if np.random.random() < self.config['orders']['arrival_rate']:
            self.dispatcher.generate_order_task()

        # === KEY FIX: Proactive task assignment every step ===
        self.dispatcher.assign_tasks()

        if not self.emergency_mode:
            # Normal mode - robots work
            for r in self.robots:
                r.step(self.env)
        else:
            # Emergency mode
            for r in self.robots:
                r.step_emergency()
            for p in self.pedestrians:
                neighbors = [other.position for other in self.pedestrians if other != p]
                p.step_evacuate(neighbors, self.sf_model, self.walls)

        # Log metrics
        if self.time % self.config['metrics']['log_interval'] == 0:
            self.metrics.log_timeseries(self.time, self.robots, self.pedestrians, self.dispatcher)

        # Trigger emergency
        if self.time == self.trigger_step and not self.emergency_mode:
            self.trigger_emergency()

        return self.time < self.max_steps

    def run(self):
        while self.step():
            if self.time % 100 == 0:
                print(f"Step {self.time} | Emergency: {self.emergency_mode} | Active orders: {len(self.dispatcher.pending_tasks)}")

        self.metrics.final_summary(self.robots, self.pedestrians, self.dispatcher, self.time)
        self.metrics.save_all()
        print("Simulation complete.")