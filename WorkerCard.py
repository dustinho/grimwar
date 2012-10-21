import json
import os

class WorkerCard:
    """
    WorkerCard is a special card. Its JSON is loaded from the /Cards/Hero
    directory
    """

    def __init__(self, name):
        spec_file = os.path.join(os.path.dirname(__file__), 'Cards/Workers', name + ".json")
        self.name = self.ammo = self.cost = self.hp = self.speed = self.damage = self.attack_pattern = attack_type = self.tier = None

        data = json.load(open(spec_file))

        for key in data:
            if hasattr(self, key):
                setattr(self, key, data[key])
