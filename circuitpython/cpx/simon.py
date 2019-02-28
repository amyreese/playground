import board
import neopixel
import random

from colors import RED, GREEN, YELLOW, BLUE, WHITE, OFF
from cpgame import after, cancel, on, start

TIMEOUT = 3

OPTIONS = {
    "blue": (BLUE, 8),
    "green": (GREEN, 6),
    "red": (RED, 3),
    "yellow": (YELLOW, 1),
}
OPTION_KEYS = list(OPTIONS.keys())
FLASH = [WHITE, OFF]

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.01, auto_write=False)
pixels.fill(OFF)
pixels.show()

READY = 1
SHOW = 2
WATCH = 3
FAIL = 4


class state:
    phase = READY
    sequence = []

    @classmethod
    def reset(cls):
        cls.phase = READY

    @classmethod
    def begin(cls):
        cls.phase = SHOW
        cls.sequence = [random.choice(OPTION_KEYS) for _ in range(3)]
        cls.pos = 0

    @classmethod
    def show(cls):
        cls.phase = SHOW
        cls.sequence.append(random.choice(OPTION_KEYS))
        cls.pos = 0

    @classmethod
    def watch(cls):
        cls.phase = WATCH
        cls.pos = 0


@on(board.A2)
def blue(now):
    press(now, "blue")


@on(board.A1)
def green(now):
    press(now, "green")


@on(board.A6)
def red(now):
    press(now, "red")


@on(board.A5)
def yellow(now):
    press(now, "yellow")


def press(now, color):
    if state.phase == READY:
        state.begin()
        cancel(ready)
        render(color)
        after(0.5, clear)
        after(1, show)

    elif state.phase == WATCH:
        if color == state.sequence[state.pos]:
            render(color)
            after(0.5, clear)
            state.pos += 1
            if state.pos == len(state.sequence):
                state.show()
                after(1, show)
                cancel(fail)
            else:
                after(TIMEOUT, fail)
        else:
            after(0, fail)


def render(name):
    pixels.fill(OFF)
    color, idx = OPTIONS[name]
    pixels[idx] = color
    pixels.show()


def clear(*args):
    pixels.fill(OFF)
    pixels.show()


def begin(now):
    state.reset()
    after(0.5, ready)
    print("ready")


def ready(now):
    pixels.fill(OFF)
    k = int(now) % 2
    for color, idx in OPTIONS.values():
        pixels[idx] = color if k else OFF
    after(0.2, ready)
    pixels.show()


def show(now):
    if state.pos < len(state.sequence):
        name = state.sequence[state.pos]
        print("show {}".format(name))
        render(name)

        state.pos += 1
        after(0.5, clear)
        after(0.75, show)
    else:
        clear()
        state.watch()
        after(TIMEOUT, fail)


def fail(now):
    print("fail")
    state.phase = FAIL
    pixels.fill(RED)
    pixels.show()
    if state.pos < 1:
        after(0.5, clear)
        after(1, fail)
        state.pos = 1
    else:
        after(0.5, clear)
        after(1, begin)


start(begin)

