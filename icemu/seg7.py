from .chip import Chip

class Segment7(Chip):
    INPUT_PINS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'DP']

    def __str__(self):
        SEGMENTS = """
 _.
|_|
|_|""".strip('\n')
        # Remember, each line is **4** chars long if we count the \n!
        SEGPOS = [
            '', 'A', 'DP', '',
            'F', 'G', 'B', '',
            'E', 'D', 'C'
        ]
        disabled_pins = {code for code in self.INPUT_PINS if self.getpin(code).ishigh()}
        return ''.join(c if seg not in disabled_pins else ' ' for c, seg in zip(SEGMENTS, SEGPOS))

