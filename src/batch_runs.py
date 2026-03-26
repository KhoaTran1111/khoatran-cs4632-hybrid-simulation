import yaml
import copy
from core.engine import SimulationEngine
import os

def run_batch():
    base_config = yaml.safe_load(open("config/simulation_config.yaml"))

    scenarios = [
        {"purpose": "Baseline", "changes": {}},
        {"purpose": "High pedestrians", "changes": {"agents": {"num_pedestrians": 80}}},
        {"purpose": "Early emergency", "changes": {"emergency": {"trigger_step": 300}}},
        {"purpose": "High orders", "changes": {"orders": {"arrival_rate": 0.15}}},
        # Add 6+ more variations...
    ]

    os.makedirs("results/batch", exist_ok=True)

    print("Running batch simulations...")
    for i, scen in enumerate(scenarios, 1):
        config = copy.deepcopy(base_config)
        # Apply changes nested
        for k, v in scen["changes"].items():
            if isinstance(v, dict):
                config[k].update(v)
            else:
                config[k] = v

        engine = SimulationEngine(config)
        engine.metrics.run_id = f"batch_{i:03d}_{scen['purpose'].replace(' ','_')}"
        engine.run()
        print(f"Run {i}/{len(scenarios)} complete: {scen['purpose']}")

if __name__ == "__main__":
    run_batch()