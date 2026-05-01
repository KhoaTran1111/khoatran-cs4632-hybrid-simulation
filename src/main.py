import yaml
from core.engine import SimulationEngine

def main():
    # Load configuration
    config_path = "config/simulation_config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    # Create and run simulation
    engine = SimulationEngine(config)
    engine.run()

    print("\nSimulation finished successfully!")

if __name__ == "__main__":
    main()