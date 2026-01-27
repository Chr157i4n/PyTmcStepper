class Pin:
    OUT = 0

    def __init__(self, pin, mode=None):
        self.pin = pin
        self.mode = mode

    def value(self, v=None):
        return 0


class PWM:
    def __init__(self, pin):
        self.pin = pin

    def freq(self, f):
        pass

    def duty_u16(self, d):
        pass
