import yaml
from core.engine import SimulationEngine
from managers.inventory import InventoryManager

def main():
    with open("config/simulation_config.yaml", "r") as f:
        config = yaml.safe_load(f)

    engine = SimulationEngine(config)
    engine.run()

if __name__ == "__main__":
    main()
    