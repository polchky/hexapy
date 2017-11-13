import machine
import servo
import ps2x_controller
import time
import math
import bloc_calculator
import ujson
import os

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
        "radian_range": 9,
        "leg_address": ["0x41", "0x40", "0x40", "0x40", "0x40", "0x41"],
        "index": {
            "inner": [6, 14, 10, 4, 0, 0],
            "coxa": [5, 13, 9, 5, 1, 1],
            "outer": [4, 12, 8, 6, 2, 2]
        },
        "offset": {
            "inner": [0, 0, 0, 0, 0, 0],
            "coxa": [0, 0, 0, 0, 0, 0],
            "outer": [0, 0, 0, 0, 0, 0]
        }
    }
}

if "config.json" in os.listdir():
    f = open("config.json", "r")
    config = ujson.loads(f.read())
    f.close()

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
    positions = [[302 for i in range(16)] for f in range(2)]
    for i in range(16):
        s1.position(i, duty=302)
        s2.position(i, duty=302)
    while True:
        if not controller.update():
            print("controller not updating")
            time.sleep(5)
            continue
        if controller.clicked("PSB_PAD_LEFT"):
            index = index if index == 0 else index - 1
            print("index: %s" % index)
        if controller.clicked("PSB_PAD_RIGHT"):
            index = index if index == 15 else index + 1
            print("index: %s" % index)
        if controller.clicked("PSB_PAD_DOWN"):
            sindex = sindex if sindex == 0 else sindex - 1
            print("s index: %s" % sindex)
        if controller.clicked("PSB_PAD_UP"):
            sindex = sindex if sindex == 15 else sindex + 1
            print("s index: %s" % sindex)
        if controller.clicked("PSB_L1"):
            positions[sindex][index] -= 3
        if controller.clicked("PSB_R1"):
            positions[sindex][index] += 3
        if controller.clicked("PSB_L2"):
            positions[sindex][index] -= 20
        if controller.clicked("PSB_R2"):
            positions[sindex][index] += 20
        s[sindex].position(index, duty=positions[sindex][index])
        if controller.clicked("PSB_CROSS"):
            print("s index: %s, index: %s / duty value: %s" % (sindex, index, positions[sindex][index]))
        time.sleep_ms(100)


def test3():

    index = 0
    t = 0
    for i in range(16):
        s1.position(i, duty=302)
        s2.position(i, duty=302)
    while True:
        time.sleep_ms(150)
        t = (t+1) % 3
        r = controller.update()
        if controller.clicked("PSB_SQUARE"):
            index -= 1
            print("index: %s" % index)
        if controller.clicked("PSB_CIRCLE"):
            index += 1
            print("index: %s" % index)
        s1.position(index, duty=(302 + (t-1) * 10))

def test4():
    global config
    s = {"0x40": s1, "0x41": s2}
    servos = ["inner", "coxa", "outer"]
    offsets = {"inner": config, "coxa": 0, "outer": 0}
    sticks = {"inner": "PSS_LX", "coxa": "PSS_RX", "outer": "PSS_RY"}
    for leg in range(6):
        sc = s[config["servos"]["leg_address"][leg]]
        for servo in servos:
            index = config["servos"]["index"][servo][leg]
            sc.position(index, duty=302 + config["servos"]["offset"][servo][leg])
    r = controller.update()
    leg = 0
    cont_middle = {
        "inner": controller.value("PSS_LX"),
        "coxa": controller.value("PSS_RX"),
        "outer": controller.value("PSS_RY")
    }
    while True:
        time.sleep_ms(100)
        r = controller.update()
        sc = s[config["servos"]["leg_address"][leg]]
        for servo in servos:
            index = config["servos"]["index"][servo][leg]
            duty = int(302 + (controller.value(sticks[servo]) - cont_middle[servo]) / 2 + config["servos"]["offset"][servo][leg])
            sc.position(index, duty=duty)
        if controller.clicked("PSB_SQUARE"):
            leg -= 1
            print("leg: %s" % leg)
        if controller.clicked("PSB_CIRCLE"):
            leg += 1
            print("leg: %s" % leg)

        if controller.clicked("PSB_R2"):
            for servo in servos:
                config["servos"]["offset"][servo][leg] = int((controller.value(sticks[servo]) - cont_middle[servo]) / 2 + config["servos"]["offset"][servo][leg])
                print(config["servos"]["offset"][servo][leg])
            time.sleep(1)
        if controller.clicked("PSB_L2"):
            print(config["servos"])
        if controller.clicked("PSB_L1"):
            print(cont_middle)
        if controller.clicked("PSB_TRIANGLE"):
            print("write config?")
            time.sleep(1)
            controller.update()
            if controller.clicked("PSB_CROSS"):
                print("writing data")
                f = open("config.json", "w")
                f.write(ujson.dumps(config))
                f.close()

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
