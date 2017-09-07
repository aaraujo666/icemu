from .chip import ActivableChip

class ShiftRegister(ActivableChip):
    SERIAL_PINS = []
    CLOCK_PIN = ''
    RESULT_PINS = [] # Data is pushed from first pin to last

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev_clock_high = False

    def update(self):
        if not self.is_enabled():
            self.setpins(self.RESULT_PINS, False)
            return

        clock = self.getpin(self.CLOCK_PIN)
        if clock.ishigh() and not self.prev_clock_high:
            val = all(self.getpin(code).ishigh() for code in self.SERIAL_PINS)
            for code in self.RESULT_PINS:
                pin = self.getpin(code)
                old = pin.ishigh()
                pin.set(val)
                val = old
        self.prev_clock_high = clock.ishigh()


class CD74AC164(ShiftRegister):
    OUTPUT_PINS = ['Q0', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7']
    INPUT_PINS = ['DS1', 'DS2', 'CP', 'MR']
    SERIAL_PINS = ['DS1', 'DS2']
    RESULT_PINS = OUTPUT_PINS
    ENABLE_PINS = ['MR']
    CLOCK_PIN = 'CP'
    STARTING_HIGH = ['MR', 'DS2']

