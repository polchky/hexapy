class Hexapod:
    class __Hexapod:
        def __init__(self):
            self.init()
            self.lol = None

        def setlol(self, value):
            self.lol = value

        def getlol(self):
            return self.lol

        def init(self):
            self.gaitmanager = False
            self.inputsource = False

        def setgaitmanager(self, gaitmanager):
            self.gaitmanager = gaitmanager

        def setinputsource(self, inputsource):
            self.inputsource = inputsource

        def start(self):
            if not self.gaitmanager :
                print("gait manager not set")
                error = True
            if not self.inputsource :
                print("input source not set")
                error = True
            if error:
                return False
            print("starting hexapod...")

            self.inputsource.setup()
            while not self.inputsource.ready():
                time.sleep(2)
                print("waiting on input source...")
            print("input source ready")

            return True

    __instance = None
    def __init__(self):
        if not Hexapod.__instance:
            Hexapod.__instance = Hexapod.__Hexapod()

    def __getattr__(self, attr):
        return getattr(Hexapod.__instance, attr)

    def __setattr__(self, attr, value):
        return setattr(Hexapod.__instance, attr, value)
