import yaml
import copy
import os
import time
from core.engine import SimulationEngine

def run_batch():
    # Load base config
    config_path = "config/simulation_config.yaml"
    with open(config_path, "r") as f:
        base_config = yaml.safe_load(f)

    scenarios = [
        {"purpose": "Baseline", "changes": {}},
        {"purpose": "High pedestrians", "changes": {"agents": {"num_pedestrians": 80}}},
        {"purpose": "Early emergency", "changes": {"emergency": {"trigger_step": 300}}},
        {"purpose": "High orders", "changes": {"orders": {"arrival_rate": 0.15}}},
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
    print("🚀 Starting Batch Simulations for Milestone 3...\n")

    results_summary = []

    for i, scen in enumerate(scenarios, 1):
        config = copy.deepcopy(base_config)

        # Apply changes
        for section, changes in scen["changes"].items():
            if section in config and isinstance(changes, dict):
                config[section].update(changes)
            else:
                config[section] = changes

        print(f"Running {i}/10: {scen['purpose']} ...")

        start_time = time.time()                    # ← Start timing

        try:
            engine = SimulationEngine(config)
            engine.metrics.run_id = f"batch_{i:03d}_{scen['purpose'].replace(' ', '_')}"
            engine.run()

            end_time = time.time()                  # ← End timing
            duration_seconds = end_time - start_time
            duration_min = duration_seconds / 60

            print(f"✅ Completed: {scen['purpose']} | Duration: {duration_min:.2f} min ({duration_seconds:.1f} sec)\n")

            # Save for final summary
            results_summary.append({
                "Run ID": f"batch_{i:03d}",
                "Purpose": scen['purpose'],
                "Key Parameters": str(scen['changes']),
                "Duration (min)": round(duration_min, 2),
                "Status": "Complete"
            })

        except Exception as e:
            end_time = time.time()
            duration_min = (end_time - start_time) / 60
            print(f"❌ Failed: {scen['purpose']} | Duration: {duration_min:.2f} min | Error: {e}\n")
            results_summary.append({
                "Run ID": f"batch_{i:03d}",
                "Purpose": scen['purpose'],
                "Key Parameters": str(scen['changes']),
                "Duration (min)": round(duration_min, 2),
                "Status": "Failed"
            })

    # Final Summary Table for your report
    print("="*80)
    print("BATCH RUN SUMMARY")
    print("="*80)
    for res in results_summary:
        print(f"{res['Run ID']:12} | {res['Purpose']:25} | {res['Duration (min)']:6.2f} min | {res['Status']}")

    print(f"\n🎉 All batch runs finished! Results saved in results/batch/")


if __name__ == "__main__":
    run_batch()