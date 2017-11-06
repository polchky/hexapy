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
        "min_us": 650,
        "max_us": 2300,
        "radian_range": 9
        "leg_address": ["0x41", "0x40", "0x40", "0x40", "0x40", "0x41"],
        "index": [
            "inner": [],
            "coxa": [],
            "outer": []
        ],
        "offset": [
            "inner": [],
            "coxa": [],
            "outer": []
        ]
    }
}

i2c = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
s1 = servo.Servos(i2c, address=0x40)
s2 = servo.Servos(i2c, address=0x41)
s = [s1, s2]

controller = ps2x_controller.Controller()

index = 0

def calibrate():
    min_duty = 133
    max_duty = 470
    index = 0
    sindex = 0
    for i in range(16):
        s1.position(i, duty=302)
        s2.position(i, duty=302)
    while True:
        if not controller.update():
            print("controller not updating")
            time.sleep(5)
            continue
        if controller.clicked("PSB_PAD_LEFT"):
            index -= 1
            print("index: %s" % index)
        if controller.clicked("PSB_PAD_RIGHT"):
            index += 1
            print("index: %s" % index)
        if controller.clicked("PSB_PAD_DOWN"):
            sindex -= 1
            print("s index: %s" % sindex)
        if controller.clicked("PSB_PAD_UP"):
            sindex += 1
            print("s index: %s" % sindex)
        if controller.clicked("PSB_L1"):
            duty = s[index].position(index) + 3
            s[sindex].position(index, duty=duty)
        if controller.clicked("PSB_R1"):
            duty = s[index].position(index) - 3
            s[sindex].position(index, duty=duty)
        if controller.clicked("PSB_L2"):
            duty = s[index].position(index) - 20
            s[sindex].position(index, duty=duty)
        if controller.clicked("PSB_R2"):
            duty = s[index].position(index) + 20
            s[sindex].position(index, duty=duty)
        if controller.clicked("PSB_CROSS"):
            print("s index: %s, index: %s / duty value: %s" % (sindex, index, s[sindex].position(index)2))






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
