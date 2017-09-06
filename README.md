# ICemu - Emulate Integrated Circuits

`icemu` is a Python library that emulates integrated circuits at the logic level. For example,
if you want to simulate a circuit with a decoder driving the clock pin of two shift registers,
it would look like this:

    dec = SN74HC138()
    sr1 = CD74AC164()
    sr2 = CD74AC164()
    mcu_pin = OutputPin('PB4')

    sr1.pin_CP.wire_to(dec.pin_Y0)
    sr2.pin_CP.wire_to(dec.pin_Y1)
    sr1.pin_DS1.wire_to(mcu_pin)
    sr2.pin_DS1.wire_to(mcu_pin)

    dec.update()
    sr1.update()
    sr2.update()

You could then play with pins at your heart contents and call `update()` when you want pin state
to "propagate" through wires and IC logic.

## What is it for

The goal of this library is to facilitate the testing and debugging of embedded software. When we
run software on an embedded prototype, it's often hard to debug failures because we don't even
know if the problem comes from hardware (wiring, it's always the wiring!) or software. Moreover,
testing directly on a prototype often involves significant setup time.

With emulation, we have a quick setup time, introspection capabilities, all this stuff. We can then
confirm the soundness of our logic before sending it to our prototype.

## Why Python

Because it's used for debugging purposes, speed is not essential. Also, Python is easy to glue
with C.

I've tried writing quick `icemu` prototype in C and Rust, but they were needlessly complicated.
With Python, it's easy to write the software and add new chips. Because there's gonna be a *lot*
of these chips to add, we might as well make this process as fast as possible.

## How to use

What you would do would be to recreate your prototype's logic in a small Python program that uses
`icemu` and wrap that into easy to use functions. Those functions should be designed to receive
pin state change from the MCU and apply the logic change into your circuit. Make that program
print relevant information so that you can assert your logic's soundness.

Then, write yourself a small Hardware Abstraction Layer at the pin/register level, embed your
Python program like a regular C application would do, make your `ifdef`ed functions call helper
functions you've written in your Python program, compile and run!

## Examples

The best place to find examples is the `tests` folders. You'll find all kinds of circuits.

## License

LGPLv3, Copyright 2017 Virgil Dupras
