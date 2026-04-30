import numpy as np
import json
import os

def calculate_95_ci(data):
    """Calculate 95% confidence interval using numpy only"""
    data = np.array(data)
    n = len(data)
    if n <= 1:
        return np.nan, np.nan
    
    mean = np.mean(data)
    std = np.std(data, ddof=1)          # sample standard deviation
    sem = std / np.sqrt(n)              # standard error
    margin = 1.96 * sem                 # 1.96 ≈ z-score for 95% CI
    
    return mean, (mean - margin, mean + margin)


def analyze_batch_results(results_dir="results/batch"):
    evac_times = []
    tasks_completed = []
    utilizations = []
    throughputs = []

    for filename in os.listdir(results_dir):
        if filename.endswith("_summary.json"):
            filepath = os.path.join(results_dir, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, dict):
                    if 'evacuation_time' in data and data['evacuation_time'] is not None:
                        evac_times.append(data['evacuation_time'])
                    if 'tasks_completed' in data:
                        tasks_completed.append(data['tasks_completed'])
                    if 'utilization' in data:
                        utilizations.append(data['utilization'])
                    if 'throughput' in data:
                        throughputs.append(data['throughput'])
            except:
                continue

    print("=== Statistical Summary (from batch results) ===\n")

    def print_stats(name, values):
        if not values:
            print(f"{name}: No data")
            return
        mean = np.mean(values)
        std = np.std(values, ddof=1)
        minimum = np.min(values)
        maximum = np.max(values)
        ci_low, ci_high = calculate_95_ci(values)
        
        print(f"{name:25} : Mean = {mean:8.2f} | Std = {std:6.2f} | "
              f"Min = {minimum:6.1f} | Max = {maximum:6.1f} | "
              f"95% CI = [{ci_low:6.1f}, {ci_high:6.1f}]  (n={len(values)})")

    print_stats("Evacuation Time (steps)", evac_times)
    print_stats("Tasks Completed", tasks_completed)
    print_stats("Robot Utilization (%)", utilizations)
    print_stats("Throughput (tasks/step)", throughputs)


if __name__ == "__main__":
    analyze_batch_results()