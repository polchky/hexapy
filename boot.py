from hexapod import Hexapod
from leg_calculator.threecoxacalculator import ThreeCoxaCalculator
from gait_manager.simplegait import SimpleGait
from input_source.bleinput import BLEInput


config = {}

hexapod = Hexapod()
lc = ThreeCoxaCalculator(config)
gait = SimpleGait(config)
gait.setlegcalculator(lc)
inputsource = BLEInput(config)

hexapod.setgaitmanager(gait)
hexapod.setinputsource(inputsource)

hexapod.start()
