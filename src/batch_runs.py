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
        {"purpose": "More Robots", "changes": {"agents": {"num_robots": 20}}},
        {"purpose": "Low Order Rate", "changes": {"orders": {"arrival_rate": 0.02}}},
        {"purpose": "Late Emergency", "changes": {"emergency": {"trigger_step": 1200}}},
        {"purpose": "Combined High Traffic", "changes": {"agents": {"num_pedestrians": 60}, "orders": {"arrival_rate": 0.12}}},
        {"purpose": "Small Grid", "changes": {"simulation": {"grid_width": 30, "grid_height": 20}}},
        {"purpose": "Large Grid", "changes": {"simulation": {"grid_width": 80, "grid_height": 50}}},

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