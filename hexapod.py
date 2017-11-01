class Hexapod():
    def __init__(self):
        self.legcalculator = False
        self.gaitmanager = False
        self.inputsource = False
        return


    def setlegcalculator(self, legcalculator):
        self.legcalculator = legcalculator

    def setgaitmanager(self, gaitmanager):
        self.gaitmanager = gaitmanager

    def setinputsource(self, inputsource):
        self.inputsource = inputsource

    def start(self):
        error = False
        if not self.legcalculator :
            print("leg calculator not set")
            error = True
        if not self.gaitmanager :
            print("gait manager not set")
            error = True
        if not self.inputsource :
            print("input source not set")
            error = True
        if error:
            return False
        print("starting")

        return True
