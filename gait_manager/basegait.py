
class BaseGait:
    def __init__(self, config):
        self.config = config
        self.direction = 0
        self.speed = 0

    def march(self, direction, speed):
        self.direction = direction
        self.speed = speed

    def turn(self, radians):
        return

    def static(self, height, direction, angle):
        return
