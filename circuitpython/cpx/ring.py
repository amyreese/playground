import board
from cpgame import tick, every, on, start, at, after
from colors import RAINBOW, WHITE, RED, GREEN, OFF
import neopixel
import random


ROUNDS = 10
SPEEDS = [0.11, 0.1, 0.1, 0.09, 0.08, 0.08, 0.07, 0.06, 0.05, 0.04]
COLORS = [WHITE] + list(reversed(RAINBOW))
REWARD = [RED, GREEN]
FLASH = [WHITE, OFF]

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.05, auto_write=False)
pixels.fill(OFF)
pixels.show()

class State:
    ready = False
    round = 0
    pos = 0
    results = []

    @classmethod
    def reset(cls):
        cls.ready = False
        cls.round = 0
        cls.pos = random.randint(0, 9)
        cls.results = [0 for i in range(ROUNDS)]

def render():
    color = COLORS[State.round]
    pixels.fill(OFF)
    pixels[State.pos] = color
    pixels.show()

@on(board.BUTTON_A)
def ready(now):
    State.ready = True

@on(board.BUTTON_B)
def play(now):
    if not State.ready:
        return

    good = 1 if State.pos == 7 else 0
    pixels.fill(REWARD[good])
    pixels[State.pos] = REWARD[not good]
    pixels.show()

    State.results[State.round] = good
    State.round += 1
    State.pos = random.randint(0, 9)

    after(0.5, main)

def finish(now):
    pixels.fill(OFF)
    for idx, value in enumerate(State.results):
        if value:
            pixels[idx] = REWARD[value] 
    pixels.show()

    State.reset()
    after(3, main)

def main(now):
    if not State.ready:
        pixels.fill(OFF)
        pixels[2] = FLASH[int(now) % 2]
        pixels.show()
        return after(0.1, main)

    if State.round >= ROUNDS:
        return after(0, finish)

    after(SPEEDS[State.round], main)
    State.pos += 1
    if State.pos >= 10:
        State.pos = 0

    render()

State.reset()
at(0, main)
start()
