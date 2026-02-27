import random
from core.environment import EnvironmentGrid
from agents.robot import Robot
from agents.pedestrian import Pedestrian
from core.engine import SimulationEngine
from managers.inventory import InventoryManager

def main():
    env = EnvironmentGrid(20, 20, obstacle_ratio=0.1)

    robots = [Robot(i, (random.randint(0,19), random.randint(0,19))) for i in range(3)]
   
    exit_pos = (10, 0)
    pedestrians = [Pedestrian(i, (random.randint(0,19), random.randint(10,19)), exit_pos)
                   for i in range(5)]

    inventory = InventoryManager()

    sim = SimulationEngine(env, robots, pedestrians, inventory, max_steps=200)
    sim.run()

if __name__ == "__main__":
    main()
