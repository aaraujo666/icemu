from itertools import chain

from .chip import Chip

class DoubleInput(Chip):
    IO_MAPPING = None # [(I1, I2, O)]

    def _test(self, pin_in1, pin_in2):
        raise NotImplementedError()

    def update(self):
        for in1, in2, out in self.IO_MAPPING:
            pin_in1 = self.getpin(in1)
            pin_in2 = self.getpin(in2)
            pin_out = self.getpin(out)
            pin_out.set(self._test(pin_in1, pin_in2))


class NOR(DoubleInput):
    def _test(self, pin_in1, pin_in2):
        return not (pin_in1.ishigh() or pin_in2.ishigh())


class CD4001B(NOR):
    IO_MAPPING = [
        ('A', 'B', 'J'),
        ('C', 'D', 'K'),
        ('G', 'H', 'M'),
        ('E', 'F', 'L'),
    ]
    INPUT_PINS = list(chain(*(t[:2] for t in IO_MAPPING)))
    OUTPUT_PINS = [t[2] for t in IO_MAPPING]


class Inverter(Chip):
    def update(self):
        for in_, out in zip(self.INPUT_PINS, self.OUTPUT_PINS):
            pin_in = self.getpin(in_)
            pin_out = self.getpin(out)
            pin_out.set(not pin_in.ishigh())


class SN74HC14(Inverter):
    INPUT_PINS = ['1A', '2A', '3A', '4A', '5A', '6A']
    OUTPUT_PINS = ['1Y', '2Y', '3Y', '4Y', '5Y', '6Y']

