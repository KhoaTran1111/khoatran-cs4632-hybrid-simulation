class Task:
    def __init__(self, task_id, item_id, location):
        self.task_id = task_id
        self.item_id = item_id
        self.location = location
        self.completed = False
