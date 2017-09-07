from icemu.pin import OutputPin
from icemu.decoders import SN74HC138
from icemu.shiftregisters import CD74AC164

def test_dec_2sr():
    # One decoder managing two SRs.
    # SRs' clock are connected to the decoder, but their DS1 is connected to the
    # same output pin.
    dec = SN74HC138()
    sr1 = CD74AC164()
    sr2 = CD74AC164()
    mcu_pin = OutputPin('PB4', True)

    def update():
        dec.update()
        sr1.update()
        sr2.update()

    sr1.pin_CP.wire_to(dec.pin_Y0)
    sr2.pin_CP.wire_to(dec.pin_Y1)
    update()
    sr1.pin_DS1.wire_to(mcu_pin)
    sr2.pin_DS1.wire_to(mcu_pin)

    update() # Y0 selected (low)
    # let's toggle SR1 CP by activating Y2
    dec.pin_B.sethigh() # Y2
    update()
    # dec.pin_B.setlow() # Y0
    # update()

    assert sr1.pin_Q0.ishigh()
    assert not sr2.pin_Q0.ishigh()
    assert not sr1.pin_Q1.ishigh()

    # SR2's turn now
    dec.pin_B.setlow()
    dec.pin_A.sethigh() # Y1 low
    update()
    dec.pin_A.setlow()
    dec.pin_B.sethigh() # Y2 low, Y1 high
    update()

    assert sr2.pin_Q0.ishigh()
    assert not sr1.pin_Q1.ishigh() # verify that we haven't pushed anything on SR1
