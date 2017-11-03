import hexapod
import calculator.bloc_calculator
import gait.simple_gait
import command.ble_command


config = {}

def start():
	hexapod = hexapod.get_hexapod()

	calculator = bloc_calculator.BlocCalculator(config)
	gait = simple_gait.SimpleGait(config)
	gait.set_calculator(calculator)
	command = ble_command.BLECommand(config)

	hexapod.set_gait(gait)
	hexapod.set_command(command)

	hexapod.start()
