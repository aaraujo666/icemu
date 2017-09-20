import random

import pytest

from icemu.shiftregisters import CD74AC164, SN74HC595

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

@pytest.mark.parametrize('sr_class,input_pin', [
    (CD74AC164, 'DS1'),
    (CD74AC164, 'DS2'),
])
def test_IO_unbuffered(sr_class, input_pin):
    sr = sr_class()

    for code in sr.SERIAL_PINS:
        pin = sr.getpin(code)
        pin.sethigh()

    val = random.randint(0, 0xff)
    push_value(sr, sr.getpin(input_pin), val)
    assert_output(sr, val)

@pytest.mark.parametrize('sr_class,input_pin', [
    (SN74HC595, 'SER'),
])
def test_IO_buffered(sr_class, input_pin):
    sr = sr_class()

    for code in sr.SERIAL_PINS:
        pin = sr.getpin(code)
        pin.sethigh()

    val = random.randint(0, 0xff)
    push_value(sr, sr.getpin(input_pin), val)
    assert_output(sr, 0)

    buffer_pin = sr.getpin(sr.BUFFER_PIN)
    buffer_pin.setlow()
    buffer_pin.sethigh()
    assert_output(sr, val)

