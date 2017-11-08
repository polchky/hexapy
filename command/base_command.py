class BaseCommand:
    _states = {"SLEEP": "sleep", "ACTIVE": "active", "EMERGENCY_STOP": "stop"}

    def __init__(self, config):
        self.config = config
        self.inputs = {
            "direction": 0,
            "walk_speed": 0,
            "walk_step": self.config["default_walk_step"]
            "turn_speed": 0,
            "turn_step": self.config["default_turn_step"]
            "turn_direction": 1,
            "state": _states["SLEEP"],
        }

    def get_input(self):
        return self.inputs

    def update(self):
        return True

    def setup(self):
        return False

    def ready(self):
        return False
