import random
from managers.task import Task

class OrderGenerator:
    def __init__(self, environment, inventory):
        self.environment = environment
        self.inventory = inventory
        self.task_counter = 0

    def generate_order(self):
        item = self.inventory.get_random_item()

        # random location in warehouse
        location = (
            random.randint(0, self.environment.width - 1),
            random.randint(0, self.environment.height - 1)
        )

        task = Task(self.task_counter, item, location)
        self.task_counter += 1

        # reduce inventory
        self.inventory.update_inventory(item, -1)

        return task
