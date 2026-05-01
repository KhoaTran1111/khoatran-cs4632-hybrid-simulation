import os
import json
import pandas as pd

class MetricsCollector:
    """Collects and saves simulation metrics"""

    def __init__(self, output_dir="results", run_id=None):
        self.output_dir = output_dir
        self.run_id = run_id or f"run_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(output_dir, exist_ok=True)
        
        self.timeseries = []
        self.summary = {}
        self.evacuation_time = None

    def log_timeseries(self, time, robots, pedestrians, dispatcher):
        data = {
            'time': time,
            'active_robots': sum(1 for r in robots if getattr(r, 'goal', None) is not None or 
                                getattr(r, 'emergency_goal', None) is not None),
            'distance_traveled_total': sum(getattr(r, 'distance_traveled', 0) for r in robots),
            'tasks_completed': sum(getattr(r, 'tasks_completed', 0) for r in robots),
            'pending_orders': len(getattr(dispatcher, 'pending_tasks', [])),
            'pedestrians_remaining': sum(1 for p in pedestrians if not getattr(p, 'evacuated', True)),
        }
        self.timeseries.append(data)

    def record_evacuation_time(self, time):
        """Record evacuation time (trigger time or completion time)"""
        self.evacuation_time = time

    def final_summary(self, robots, pedestrians, dispatcher, final_time):
        total_tasks = sum(getattr(r, 'tasks_completed', 0) for r in robots)
        num_robots = len(robots)
        
        self.summary = {
            'total_steps': final_time,
            'evacuation_time': self.evacuation_time if self.evacuation_time is not None else "Not triggered",
            'evacuation_status': "Complete" if (self.evacuation_time and 
                                               sum(1 for p in pedestrians if not getattr(p, 'evacuated', False)) == 0) else "Incomplete",
            'tasks_completed': total_tasks,
            'total_distance': sum(getattr(r, 'distance_traveled', 0) for r in robots),
            'utilization': round((total_tasks / (num_robots * final_time) * 100), 2) if final_time > 0 else 0.0,
            'throughput': round(total_tasks / final_time, 4) if final_time > 0 else 0.0,
            'pending_orders': len(getattr(dispatcher, 'pending_tasks', [])),
            'robots_count': num_robots,
        }

    def save_all(self):
        # Save time-series
        if self.timeseries:
            df = pd.DataFrame(self.timeseries)
            df.to_csv(os.path.join(self.output_dir, f"{self.run_id}_timeseries.csv"), index=False)

        # Save summary
        with open(os.path.join(self.output_dir, f"{self.run_id}_summary.json"), 'w') as f:
            json.dump(self.summary, f, indent=2)

        print(f"✅ Results saved for run: {self.run_id}")