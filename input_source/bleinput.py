from .baseinput import BaseInput

class BLEInput(BaseInput):
    def __init__(self, config):
        super().__init__(config)

    def setup(self):
        return 1

    def ready(self):
        return True
