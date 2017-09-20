import random

import pytest

from icemu.gates import SN74HC14

def assert_output(sr, expected_value):
    value = 0
    for index, code in enumerate(sr.OUTPUT_PINS):
        pin = sr.getpin(code)
        if pin.ishigh():
            value |= 1 << index
    assert expected_value == value

def push_value(sr, input_pin, value):
    clock_pin = sr.getpin(sr.CLOCK_PIN)
    for index in range(len(sr.OUTPUT_PINS)):
        input_pin.set(bool(value & (1 << (len(sr.OUTPUT_PINS) - index - 1))))
        clock_pin.setlow()
        clock_pin.sethigh()

@pytest.mark.parametrize('inv_class', [
    SN74HC14
])
def test_inverters(inv_class):
    inv = inv_class()

    val = random.randint(0, 0xff)

    for i, in_ in enumerate(inv.INPUT_PINS):
        pin = inv.getpin(in_)
        pin.set(bool(val & (1 << i)))

    inv.update()

    for i, out in enumerate(inv.OUTPUT_PINS):
        pin = inv.getpin(out)
        assert pin.ishigh() == (not bool(val & (1 << i)))

