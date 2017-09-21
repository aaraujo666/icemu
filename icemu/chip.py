from .pin import Pin

class Chip:
    OUTPUT_PINS = []
    INPUT_PINS = []
    STARTING_HIGH = [] # pins that start high

    def __init__(self):
        for code in self.OUTPUT_PINS:
            pin = Pin(code, chip=self, output=True, high=(code in self.STARTING_HIGH))
            setattr(self, 'pin_{}'.format(code), pin)
        for code in self.INPUT_PINS:
            pin = Pin(code, chip=self, high=(code in self.STARTING_HIGH))
            setattr(self, 'pin_{}'.format(code), pin)
        self.update()

    def __str__(self):
        inputs = ' '.join(str(self.getpin(code)) for code in self.INPUT_PINS)
        outputs = ' '.join(str(self.getpin(code)) for code in self.OUTPUT_PINS)
        return '{} I: {} O: {}'.format(self.__class__.__name__, inputs, outputs)

    def getpin(self, code):
        return getattr(self, 'pin_{}'.format(code))

    def getpins(self, codes):
        return (self.getpin(code) for code in codes)

    # Set multiple pins on the same chip and only update chips one all pins are updated.
    def setpins(self, low, high):
        updateself = False
        updatelist = set()
        for codes, val in [(low, False), (high, True)]:
            for pin in self.getpins(codes):
                if pin.high != val:
                    pin.high = val
                    if pin.output:
                       updatelist |= pin.propagate_to()
                    else:
                        updateself = True
        if updateself:
            self.update()
        for chip in updatelist:
            chip.update()

    def update(self):
        pass

    # Same as with setpins, but for wire_to()
    # Has to be called from the chip having the *input* pins
    def wirepins(self, chip, inputs, outputs):
        for icode, ocode in zip(inputs, outputs):
           ipin = self.getpin(icode)
           opin = chip.getpin(ocode)
           assert opin.output
           assert not ipin.output
           ipin.wires.add(opin)
           opin.wires.add(ipin)
        self.update()

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

