from .base_gait import BaseGait

class SimpleGait(BaseGait):
    def __init__(self, config):
        BaseGait.__init__(config)

    def set_calculator(self, calculator):
        self.calculator = calculator
