import machine
import servo
import ps2x_controller
import time
import math
import bloc_calculator
import ujson
import os

if "config.json" in os.listdir():
    f = open("config.json", "r")
    config = ujson.loads(f.read())
    f.close()
else:
    print("no config file")

i2c = machine.I2C(sda=machine.Pin(21), scl=machine.Pin(22))
s1 = servo.Servos(i2c, address=0x40)
s2 = servo.Servos(i2c, address=0x41)
s = [s1, s2]

controller = ps2x_controller.Controller()

def calibrate():
    global config
    s = {"0x40": s1, "0x41": s2}
    servos = ["inner", "coxa", "outer"]
    offsets = {"inner": config, "coxa": 0, "outer": 0}
    sticks = {"inner": "PSS_LX", "coxa": "PSS_RX", "outer": "PSS_RY"}
    for leg in range(6):
        sc = s[config["servos"]["leg_address"][leg]]
        for servo in servos:
            index = config["servos"]["index"][servo][leg]
            sc.position(index, duty=302 + config["servos"]["offset_duty"][servo][leg])
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
            duty = int(302 + (controller.value(sticks[servo]) - cont_middle[servo]) / 5 + config["servos"]["offset_duty"][servo][leg])
            sc.position(index, duty=duty)
        if controller.clicked("PSB_SQUARE"):
            leg -= 1
            print("leg: %s" % leg)
        if controller.clicked("PSB_CIRCLE"):
            leg += 1
            print("leg: %s" % leg)

        if controller.clicked("PSB_R2"):
            for servo in servos:
                config["servos"]["offset_duty"][servo][leg] = int((controller.value(sticks[servo]) - cont_middle[servo]) / 5 + config["servos"]["offset_duty"][servo][leg])
                print(config["servos"]["offset_duty"][servo][leg])
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

def get_offset():
    bc = bloc_calculator.BlocCalculator(config["dimensions"])
    f = open("calibration.json")
    c = ujson.loads(f.read())
    f.close()
    result = {}
    print(bc.get_angles(c["x"][1], c["y"][1], c["z"][1], 1))
