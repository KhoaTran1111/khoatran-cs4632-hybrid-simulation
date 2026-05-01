import yaml
import copy
import os
import time
from core.engine import SimulationEngine

def run_batch():
    config_path = "config/simulation_config.yaml"
    with open(config_path, "r") as f:
        base_config = yaml.safe_load(f)

    # Define different scenarios
    scenarios = [
        {"purpose": "Baseline", "changes": {}},
        {"purpose": "High Pedestrians", "changes": {"agents": {"num_pedestrians": 80}}},
        {"purpose": "Early Emergency", "changes": {"emergency": {"trigger_step": 300}}},
        {"purpose": "High Order Rate", "changes": {"orders": {"arrival_rate": 0.15}}},
        {"purpose": "More Robots", "changes": {"agents": {"num_robots": 20}}},
        {"purpose": "Low Order Rate", "changes": {"orders": {"arrival_rate": 0.02}}},
        {"purpose": "Late Emergency", "changes": {"emergency": {"trigger_step": 1200}}},
        {"purpose": "Combined High Traffic", "changes": {
            "agents": {"num_pedestrians": 60},
            "orders": {"arrival_rate": 0.12}
        }},
        {"purpose": "Small Grid", "changes": {"simulation": {"grid_width": 30, "grid_height": 20}}},
        {"purpose": "Large Grid", "changes": {"simulation": {"grid_width": 80, "grid_height": 50}}},
    ]

    os.makedirs("results/batch", exist_ok=True)
    print("🚀 Starting Batch Simulations...\n")

    for i, scen in enumerate(scenarios, 1):
        config = copy.deepcopy(base_config)

        # Apply changes
        for section, changes in scen["changes"].items():
            if section in config and isinstance(changes, dict):
                config[section].update(changes)
            else:
                config[section] = changes

        print(f"Running {i}/10: {scen['purpose']} ...")

        start_time = time.time()

        try:
            engine = SimulationEngine(config)
            # Set custom run_id for easier identification
            engine.metrics.run_id = f"batch_{i:03d}_{scen['purpose'].replace(' ', '_')}"
            engine.run()

            duration = time.time() - start_time
            print(f"✅ Completed: {scen['purpose']} | Duration: {duration:.1f} seconds\n")

        except Exception as e:
            duration = time.time() - start_time
            print(f"❌ Failed: {scen['purpose']} | Duration: {duration:.1f}s | Error: {e}\n")

    print("🎉 All batch runs completed! Check the 'results/batch/' folder.")


if __name__ == "__main__":
    run_batch()