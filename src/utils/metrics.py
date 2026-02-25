class Metrics:
    def __init__(self):
        self.robot_distance = 0
        self.evacuation_time = None

    def record_robot(self, robots):
        self.robot_distance = sum(r.distance_traveled for r in robots)

    def record_evacuation(self, time):
        self.evacuation_time = time

    def report(self):
        print("=== METRICS ===")
        print("Total Robot Distance:", self.robot_distance)
        print("Evacuation Time:", self.evacuation_time)
