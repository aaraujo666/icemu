import pytest

from icemu.pin import pinrange
from icemu.decoders import SN74HC138

def assert_pin_is_selected(dec, selected_pin):
    for index, code in enumerate(pinrange('Y', 0, 7)):
        pin = dec.getpin(code)
        assert pin.ishigh() == (index != selected_pin)

@pytest.mark.parametrize('input_value,selected_pin', [
    (0b000, 0),
    (0b001, 1),
    (0b010, 2),
    (0b011, 3),
    (0b100, 4),
    (0b101, 5),
    (0b110, 6),
    (0b111, 7),
])
def test_SN74HC138_IO(input_value, selected_pin):
    # make sure that outputs correspond to inputs
    dec = SN74HC138()

    dec.pin_A.set(bool(input_value & 0b001))
    dec.pin_B.set(bool(input_value & 0b010))
    dec.pin_C.set(bool(input_value & 0b100))

    assert_pin_is_selected(dec, selected_pin)

def test_SN74HC138_initial():
    dec = SN74HC138()

    assert_pin_is_selected(dec, 0)

@pytest.mark.parametrize('enable_pin,disabled_value', [
    ('G1', False),
    ('G2A', True),
    ('G2B', True),
])
def test_SN74HC138_disabled(enable_pin, disabled_value):
    # no pin is selected when disabled

    dec = SN74HC138()
    dec.getpin(enable_pin).set(disabled_value)

    assert_pin_is_selected(dec, -1)
