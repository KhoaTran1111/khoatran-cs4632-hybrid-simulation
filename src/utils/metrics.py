import os
import json
import pandas as pd

class MetricsCollector:
    def __init__(self, output_dir, start_time=0):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.run_id = f"run_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
        self.timeseries = []
        self.evacuation_time = None
        self.summary = {}

    def log_timeseries(self, time, robots, pedestrians, dispatcher):
        data = {
            'time': time,
            'active_robots': len([r for r in robots if r.goal is not None]),
            'distance_traveled_total': sum(r.distance_traveled for r in robots),
            'tasks_completed': sum(r.tasks_completed for r in robots),
            'pending_orders': len(dispatcher.pending_tasks),
            'pedestrians_remaining': sum(1 for p in pedestrians if not p.evacuated),
        }
        self.timeseries.append(data)

    def record_evacuation_time(self, time):
        self.evacuation_time = time

    def final_summary(self, robots, pedestrians, dispatcher, final_time):
        self.summary = {
            'total_steps': final_time,
            'evacuation_time': self.evacuation_time if self.evacuation_time else "Incomplete",
            'total_distance_robots': sum(r.distance_traveled for r in robots),
            'tasks_completed': sum(r.tasks_completed for r in robots),
            'orders_generated': dispatcher.task_counter,
            'utilization': sum(r.tasks_completed for r in robots) / (len(robots) * final_time / 100) if final_time > 0 else 0,
            'throughput': dispatcher.completed_tasks / final_time if final_time > 0 else 0,
        }

    def save_all(self):
        df_ts = pd.DataFrame(self.timeseries)
        df_ts.to_csv(os.path.join(self.output_dir, f"{self.run_id}_timeseries.csv"), index=False)

        with open(os.path.join(self.output_dir, f"{self.run_id}_summary.json"), 'w') as f:
            json.dump(self.summary, f, indent=2)

        print(f"Results saved to {self.output_dir}")