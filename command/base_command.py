class BaseCommand:
    def __init__(self, config):
        self.config = config

    def get_input(self):
        return

    def setup(self):
        return False

    def ready(self):
        return False


class _CommandInputs():

    self.command_keys_ = {
        "direction": 0,
        "speed": 0,
        "turn_step",
        "turn_direction",
        "click_sleep",
        "click_wake_up",
        "click_emergency_stop"]

    def __init__(self):
        self

    def update(self, values):
