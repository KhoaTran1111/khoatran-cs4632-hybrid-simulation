import numpy as np
import json
import os
from pathlib import Path

def calculate_95_ci(data):
    """Calculate mean and 95% confidence interval using numpy only"""
    data = np.array(data, dtype=float)
    n = len(data)
    if n <= 1:
        return float('nan'), (float('nan'), float('nan'))
    
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    sem = std / np.sqrt(n)
    margin = 1.96 * sem                    # 1.96 for 95% CI
    
    return mean, (mean - margin, mean + margin)


def analyze_results(results_dir="results/batch"):
    print("=" * 70)
    print("📊 STATISTICAL ANALYSIS OF BATCH RUNS")
    print("=" * 70)

    evac_times = []
    tasks_list = []
    util_list = []
    throughput_list = []

    results_path = Path(results_dir)
    if not results_path.exists():
        print(f"❌ Directory '{results_dir}' not found.")
        return

    for file in results_path.iterdir():
        if file.name.endswith("_summary.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, dict):
                    if isinstance(data.get('evacuation_time'), (int, float)):
                        evac_times.append(data['evacuation_time'])
                    if isinstance(data.get('tasks_completed'), (int, float)):
                        tasks_list.append(data['tasks_completed'])
                    if isinstance(data.get('utilization'), (int, float)):
                        util_list.append(data['utilization'])
                    if isinstance(data.get('throughput'), (int, float)):
                        throughput_list.append(data['throughput'])
            except Exception:
                continue

    def print_metric(name, values):
        if not values:
            print(f"{name:25} : No data available")
            return
        
        mean = np.mean(values)
        std = np.std(values, ddof=1)
        min_val = np.min(values)
        max_val = np.max(values)
        mean_ci, (low, high) = calculate_95_ci(values)
        
        print(f"{name:25} : Mean = {mean:8.2f} | Std = {std:6.2f} | "
              f"Min = {min_val:6.1f} | Max = {max_val:6.1f} | "
              f"95% CI = [{low:6.1f}, {high:6.1f}]  (n={len(values)})")

    print_metric("Evacuation Time (steps)", evac_times)
    print_metric("Tasks Completed", tasks_list)
    print_metric("Robot Utilization (%)", util_list)
    print_metric("Throughput (tasks/step)", throughput_list)

    print("\n" + "="*70)
    print("Analysis complete. Use these values in your M5 report.")


if __name__ == "__main__":
    analyze_results()