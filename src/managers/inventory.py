import random

class InventoryManager:
    def __init__(self):
        # item_id -> quantity
        self.inventory = {
            "A": 20,
            "B": 15,
            "C": 10
        }

        # reorder points
        self.reorder_points = {
            "A": 5,
            "B": 5,
            "C": 3
        }

        # reorder quantity (Q)
        self.reorder_quantity = {
            "A": 15,
            "B": 10,
            "C": 8
        }

        self.emergency_mode = False

    def update_inventory(self, item_id, change):
        if item_id not in self.inventory:
            return

        self.inventory[item_id] += change

        if self.inventory[item_id] <= self.reorder_points[item_id]:
            self.trigger_reorder(item_id)

    def trigger_reorder(self, item_id):
        print(f"Reordering item {item_id}")
        self.inventory[item_id] += self.reorder_quantity[item_id]

    def set_emergency_mode(self, enabled):
        self.emergency_mode = enabled

    def get_random_item(self):
        return random.choice(list(self.inventory.keys()))
