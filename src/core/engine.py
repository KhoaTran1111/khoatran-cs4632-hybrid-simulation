import numpy as np
import random
from agents.robot import Robot
from agents.pedestrian import Pedestrian
from algorithms.social_force import SocialForceModel
from managers.task_dispatcher import TaskDispatcher
from core.environment import EnvironmentGrid
from utils.metrics import MetricsCollector


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

        self.env = EnvironmentGrid(self.grid_w, self.grid_h, self.walls)

        # Agents
        self.robots = []
        self.pedestrians = []
        self._init_agents()

        # Models and Managers
        self.sf_model = SocialForceModel()
        self.dispatcher = TaskDispatcher(self.robots, self.env)

        # Metrics
        self.metrics = MetricsCollector(
            output_dir=config.get('metrics', {}).get('output_dir', 'results'),
            run_id=None
        )

        # Set random seeds for reproducibility
        random.seed(config['simulation'].get('random_seed', 42))
        np.random.seed(config['simulation'].get('random_seed', 42))

    def _init_agents(self):
        """Initialize robots and pedestrians"""
        # Robots
        for i in range(self.config['agents']['num_robots']):
            pos = [random.randint(2, self.grid_w - 3), random.randint(2, self.grid_h - 3)]
            self.robots.append(Robot(i, pos))

        # Pedestrians
        for i in range(self.config['agents']['num_pedestrians']):
            pos = [random.randint(5, self.grid_w - 6), random.randint(5, self.grid_h - 6)]
            exit_pos = random.choice(self.exits)
            self.pedestrians.append(Pedestrian(i, pos, exit_pos))

    def trigger_emergency(self):
        print(f"EMERGENCY TRIGGERED at step {self.time}")
        self.emergency_mode = True
        for r in self.robots:
            nearest_safe = self._get_nearest_safe_zone(r.position)
            r.emergency_retreat(nearest_safe, self.env)

    def _get_nearest_safe_zone(self, pos):
        safe_zones = self.config['emergency'].get('safe_zones', [[0, 0], [0, self.grid_h-1],
                                                                 [self.grid_w-1, 0], [self.grid_w-1, self.grid_h-1]])
        dists = [np.linalg.norm(np.array(pos) - np.array(s)) for s in safe_zones]
        return safe_zones[np.argmin(dists)]

    def step(self):
        self.time += 1

        # Generate new orders using Poisson process
        if np.random.random() < self.config['orders'].get('arrival_rate', 0.05):
            self.dispatcher.generate_order_task()

        # Proactive task assignment
        self.dispatcher.assign_tasks()

        if not self.emergency_mode:
            # Normal operation: robots work on tasks
            for robot in self.robots:
                robot.step(self.env)
        else:
            # Emergency mode: robots retreat, pedestrians evacuate
            for robot in self.robots:
                robot.step_emergency()
            for ped in self.pedestrians:
                neighbors = [other.position for other in self.pedestrians if other != ped]
                ped.step_evacuate(neighbors, self.sf_model, self.walls)

        # Record metrics periodically
        if self.time % self.config['metrics'].get('log_interval', 10) == 0:
            self.metrics.log_timeseries(self.time, self.robots, self.pedestrians, self.dispatcher)

        # Trigger emergency at specified step
        if self.time == self.trigger_step and not self.emergency_mode:
            self.trigger_emergency()

        # Check if simulation should end
        if self.emergency_mode and all(p.evacuated for p in self.pedestrians):
            self.metrics.record_evacuation_time(self.time)
            return False

        return self.time < self.max_steps

    def run(self):
        print(f"Starting simulation with {len(self.robots)} robots and {len(self.pedestrians)} pedestrians...\n")

        emergency_triggered_at = None

        while self.step():
            if self.time % 200 == 0 or self.time == self.trigger_step:
                peds_left = sum(1 for p in self.pedestrians if not getattr(p, 'evacuated', False))
                print(f"Step {self.time:4d} | Emergency: {self.emergency_mode} | "
                      f"Active Robots: {sum(1 for r in self.robots if getattr(r, 'is_busy', lambda: False)())} | "
                      f"Pedestrians Left: {peds_left}")

            # Trigger emergency
            if self.time == self.trigger_step and not self.emergency_mode:
                self.trigger_emergency()
                emergency_triggered_at = self.time

        # === FINAL EVACUATION LOGIC - FIXED ===
        peds_remaining = sum(1 for p in self.pedestrians if not getattr(p, 'evacuated', False))

        if emergency_triggered_at is not None:
            if peds_remaining == 0:
                self.metrics.record_evacuation_time(self.time)
                status = f"Completed at step {self.time}"
            else:
                self.metrics.record_evacuation_time(emergency_triggered_at)
                status = f"Triggered at step {emergency_triggered_at} ({peds_remaining} peds remaining)"
            print(f"Evacuation Status: {status}")
        else:
            print("Evacuation Time: Not triggered")

        # Save final metrics
        self.metrics.final_summary(self.robots, self.pedestrians, self.dispatcher, self.time)
        self.metrics.save_all()

        print("\n" + "="*70)
        print(f"SIMULATION FINISHED | Total Steps: {self.time}")
        print(f"Final Evacuation Time : {self.metrics.evacuation_time}")
        print("="*70)