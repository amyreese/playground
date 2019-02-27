"""
Colorful binary counter for CPX.
Left button pauses or upauses the counter.
Right button cycles colors.
Both buttons together resets the counter.
"""

import time
import board
from digitalio import DigitalInOut, Direction, Pull
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

btn_a = DigitalInOut(board.BUTTON_A)
btn_a.direction = Direction.INPUT
btn_a.pull = Pull.DOWN

btn_b = DigitalInOut(board.BUTTON_B)
btn_b.direction = Direction.INPUT
btn_b.pull = Pull.DOWN

pxc = 10
pixels = neopixel.NeoPixel(board.NEOPIXEL, pxc, brightness=0.05, auto_write=False)
pixels.fill(OFF)
pixels.show()

def next_color():
    while True:
        for color in COLORS:
            yield color

counter = -1
step = 1
interval = 1.0
colorgen = next_color()
color = next(colorgen)
target = time.monotonic()
while True:
    if btn_a.value and btn_b.value:
        counter = 0
        step = 1
    elif btn_b.value:
        color = next(colorgen)
    elif btn_a.value:
        step = 0 if step else 1

    counter += step
    if counter < 0:
        counter = (2 ** pxc) - 1
    elif counter >= (2 ** pxc):
        counter = 0

    print(counter, step, color)
    for i in range(pxc):
        pixels[i] = color if counter & (2**i) else OFF
    pixels.show()

    target += interval
    now = time.monotonic()
    slp = target - now
    while slp > 0:
        time.sleep(slp)
        now = time.monotonic()
        slp = target - now
