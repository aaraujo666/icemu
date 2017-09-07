class Pin:
    def __init__(self, code, high=False):
        self.code = code
        self.high = high

    def __str__(self):
        return '{}/{}'.format(self.code, 'H' if self.ishigh() else 'L')

    def ishigh(self):
        return self.high

    def set(self, val):
        self.high = val

    def sethigh(self):
        self.set(True)

    def setlow(self):
        self.set(False)

    def toggle(self):
        self.set(not self.ishigh())

class OutputPin(Pin): pass

class InputPin(Pin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wires = []

    def wire_to(self, output_pin):
        assert isinstance(output_pin, OutputPin)
        self.wires.append(output_pin)

    def ishigh(self):
        if self.wires:
            return any(p.ishigh() for p in self.wires)
        else:
            return self.high

