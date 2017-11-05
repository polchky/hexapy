import machine
import servo
import ps2x_controller
import time
import math
import bloc_calculator

config = {
    "dimensions": {
        "gx": [0,85],
        "gy": [0,0],
        "gz": [0,0],
        "go": [0,0],
        "gh": 19.2,
        "haxy": -12,
        "haz": 14,
        "hbxy": 12,
        "hbz": 14,
        "ac": 55,
        "cd": 50,
        "be": 40,
        "de": 40,
        "ef": 92
    },
    "servos": {
        "address": [

        ],
        "index": [

        ]

    }
}

i2c = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
s1 = servo.Servos(i2c, address=0x40)
s2 = servo.Servos(i2c, address=0x41)

controller = ps2x_controller.Controller()

index = 0

def calibrate():


def test2():

    bc = bloc_calculator.BlocCalculator(config)
    base_height = -70
    amp = 20
    step = 0
    while True:
        step = (step + 0.1) % (2 * math.pi)
        height = base_height + math.cos(step) * amp
        s1 = bc.get_angles(135, 0, height, 1)


        time.sleep_ms(40)
