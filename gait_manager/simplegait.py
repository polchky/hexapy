from .basegait import BaseGait

class SimpleGait(BaseGait):
    def __init__(self, config):
        super().__init__(config)

    def setlegcalculator(self, legcalculator):
        self.legcalculator = legcalculator
