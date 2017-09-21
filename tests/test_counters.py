import random

import pytest

from icemu.counters import SN74F161AN
from icemu.util import get_binary_value

@pytest.mark.parametrize('cnt_class', [
    SN74F161AN,
])
def test_counters(cnt_class):
    cnt = cnt_class()

    clk = cnt.getpin(cnt.CLOCK_PIN)
    val = random.randint(0, cnt.maxvalue())
    for _ in range(val):
        clk.setlow()
        clk.sethigh()

    assert get_binary_value(cnt.getpins(cnt.OUTPUT_PINS)) == val

