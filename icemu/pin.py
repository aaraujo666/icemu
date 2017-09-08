class Pin:
    def __init__(self, code, high=False, chip=None, output=False):
        self.code = code
        self.high = high
        self.chip = chip
        self.output = output
        self.wires = set()

    def __str__(self):
        return '{}/{}'.format(self.code, 'H' if self.ishigh() else 'L')

    def ishigh(self):
        if not self.output and self.wires:
            wired_outputs = (p for p in self.wires if p.output)
            return any(p.ishigh() for p in wired_outputs)
        else:
            return self.high

    def propagate_to(self):
        if self.output:
            return {
                p.chip for p in self.wires
                if not p.output and p.chip is not self and p.chip is not None
            }
        else:
            return set()

    # The dont_update_self is used when we set pins during update() to avoid recursion.
    def set(self, val, dont_update_self=False):
        if val == self.high:
            return

        self.high = val
        if self.chip and not dont_update_self:
            self.chip.update()

        if self.output:
            wired_chips = self.propagate_to()
            for chip in wired_chips:
                chip.update()

    def sethigh(self):
        self.set(True)

    def setlow(self):
        self.set(False)

    def toggle(self):
        self.set(not self.ishigh())

    def wire_to(self, output_pin):
        assert not self.output
        assert output_pin.output
        self.wires.add(output_pin)
        output_pin.wires.add(self)
        if self.chip:
            self.chip.update()

