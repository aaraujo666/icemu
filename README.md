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

    print(dec.asciiart())
         _______
       A>|- U +|>Y7
       B>|-   +|>Y6
       C>|-   +|>Y5
     G2A>|-   +|>Y4
     G2B>|-   +|>Y3
      G1>|+   +|>Y2
      Y0<|-___+|>Y1

You could then play with pins at your heart contents and have them "propagate" through wires and IC
logic automatically.

## See it in action

Here's a little video of `icemu` used in my [seg7-multiplex][seg7-multiplex] project:

[![asciinema](https://asciinema.org/a/WsYhXc1VcgfmkKZ8SAT18xYjv.png)](https://asciinema.org/a/WsYhXc1VcgfmkKZ8SAT18xYjv)

That timer has 3 7-segments led matrices driven my 3 shift registers themselves driven by a 3-8
decoder. These are all emulated in a virtual circuit and the output is the output of the led
matrices themselves.

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

You can install `icemu` with pip on python **3.4+**:

    $ pip install --user icemu

Then, you need to recreate your prototype's logic in a small Python program that uses `icemu` and
wrap that into easy to use functions. Those functions should be designed to receive pin state
change from the MCU and apply the logic change into your circuit. Make that program print relevant
information so that you can assert your logic's soundness.

Then, write yourself a small Hardware Abstraction Layer at the pin/register level, embed your
Python program like a regular C application would do, make your `ifdef`ed functions call helper
functions you've written in your Python program, compile and run!

## Examples

You can find small examples is the `tests` folders, but the best way to get the grand idea is to
look at a project that uses it such as my [seg7-multiplex][seg7-multiplex] or my 
[solar-timer][solar-timer]. Read the Simulation part of the README to get started.

## License

LGPLv3, Copyright 2017 Virgil Dupras

[solar-timer]: https://github.com/hsoft/solar-timer
[seg7-multiplex]: https://github.com/hsoft/seg7-multiplex
