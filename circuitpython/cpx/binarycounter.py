"""
Colorful binary counter for CPX.
Left button pauses or upauses the counter.
Right button cycles colors.
Both buttons together resets the counter.
"""

import cpgame
import board
import neopixel

RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
LIME = (150, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 150)
BLUE = (0, 0, 255)
INDIGO = (100, 0, 255)
VIOLET = (255, 0, 255)
OFF = (0,0,0)

COLORS = [RED, ORANGE, YELLOW, LIME, GREEN, CYAN, BLUE, INDIGO, VIOLET]

pxc = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, pxc, brightness=0.05, auto_write=False)
pixels.fill(OFF)
pixels.show()

def next_color():
    while True:
        for color in COLORS:
            yield color

class State:
    pass

state = State()
state.counter = -1
state.step = 1
state.colors = next_color()
state.color = next(state.colors)

def render():
    # print(state.counter, state.step, state.color)
    for i in range(pxc):
        pixels[i] = state.color if state.counter & (2**i) else OFF
    pixels.show()

@cpgame.on(board.BUTTON_A, board.BUTTON_B)
def button_a(now):
    print("reset")
    state.counter = 0
    state.step = 1

@cpgame.on(board.BUTTON_A)
def button_a(now):
    print("next color")
    state.color = next(state.colors)
    render()

@cpgame.on(board.BUTTON_B)
def button_a(now):
    if state.step:
        print("pause")
        state.step = 0
    else:
        print("resume")
        state.step = 1

# @cpgame.every(0.1)
def buttons(now):
    if btn_a.value and btn_b.value:
        state.counter = 0
        state.step = 1
        cpgame.stop()
    elif btn_b.value:
        state.color = next(state.colors)
    elif btn_a.value:
        state.step = 0 if state.step else 1

    render()

@cpgame.every(1)
def count(now):
    state.counter += state.step
    if state.counter < 0:
        state.counter = (2 ** pxc) - 1
    elif state.counter >= (2 ** pxc):
        state.color = next(state.colors)
        state.counter = 0

    render()

if __name__ == "__main__":
    cpgame.start()
