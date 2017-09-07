from .pin import OutputPin, InputPin

class Chip:
    OUTPUT_PINS = []
    INPUT_PINS = []
    STARTING_HIGH = [] # pins that start high

    def __init__(self):
        for code in self.OUTPUT_PINS:
            setattr(self, 'pin_{}'.format(code), OutputPin(code))
        for code in self.INPUT_PINS:
            setattr(self, 'pin_{}'.format(code), InputPin(code))
        for code in self.STARTING_HIGH:
            pin = self.getpin(code)
            pin.sethigh()

    def __str__(self):
        inputs = ' '.join(str(self.getpin(code)) for code in self.INPUT_PINS)
        outputs = ' '.join(str(self.getpin(code)) for code in self.OUTPUT_PINS)
        return '{} I: {} O: {}'.format(self.__class__.__name__, inputs, outputs)

    def getpin(self, code):
        return getattr(self, 'pin_{}'.format(code))

    def setpins(self, codes, high):
        for code in codes:
            pin = self.getpin(code)
            pin.set(high)


class ActivableChip(Chip):
    ENABLE_PINS = [] # ~ means that low == enabled

    def is_enabled(self):
        for code in self.ENABLE_PINS:
            pin = self.getpin(code.replace('~', ''))
            enabled = pin.ishigh()
            if code.startswith('~'):
                enabled = not enabled
            if not enabled:
                return False
        return True

