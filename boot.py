from hexapod import Hexapod
from leg_calculator.threecoxacalculator import ThreeCoxaCalculator
from gait_manager.simplegait import SimpleGait
from input_source.bleinput import BLEInput


config = {}

hexapod = Hexapod()
hexapod.setlegcalculator(ThreeCoxaCalculator(config))
hexapod.setgaitmanager(SimpleGait(config))
hexapod.setinputsource(BLEInput(config))

hexapod.start()
