import time


class _Hexapod:
    def __init__(self):
        self.gait = None
        self.command = None

    def set_gait(self, gait):
        self.gait = gait

    def set_command(self, command):
        self.command = command

    def start(self):
        if not self.gait :
            print("gait not set")
            return False
        if not self.command :
            print("command not set")
            return False

        print("starting hexapod...")

        self.command.setup()
        while not self.command.ready():
            time.sleep(2)
            print("waiting on command...")
        print("command ready")

        return True


hexapod = _Hexapod()

def get_hexapod():
    return hexapod
