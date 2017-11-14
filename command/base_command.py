class BaseCommand:

    STICK_LX = "STICK_LX"
    STICK_LY = "STICK_LY"
    STICK_RX = "STICK_RX"
    STICK_RY = "STICK_RY"

    BTN_SLEEP = "BTN_SLEEP"
    BTN_EMERGENCY_STOP = "BTN_EMERGENCY_STOP"
    BTN_WAKE_UP = "BTN_WAKE_UP"
    


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

    def clicked(self, button):
        return True

    def value(self, input):
        return 0
