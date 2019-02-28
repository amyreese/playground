import board
import neopixel

from colors import RAINBOW, BLUE, YELLOW, WHITE
from cpgame import after, start

STEP = 1.0 / 256
UPPER = STEP * 30
LOWER = STEP * 2
START = LOWER

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=START)
# pixels.fill(WHITE)
pixels.fill(BLUE)
pixels[3], pixels[4], pixels[8], pixels[9] = YELLOW, YELLOW, YELLOW, YELLOW

class state:
    value = START
    step = STEP
    bottom = 0
    duration = 0

def reset(now):
    state.bottom = now
    state.duration = 0

def main(now):
    b = pixels.brightness
    n = ((UPPER - b) ** 1.5)
    m = ((b - LOWER) ** 2)
    delay = 4.5 * (n + m)

    if b >= UPPER and state.step > 0:
        state.step = -state.step
        delay = 0.3

    if b <= LOWER and state.step < 0:
        state.step = -state.step
        state.duration = now - state.bottom
        state.bottom = now
        print("breath took {} seconds".format(state.duration))
        delay = 0.3
    
    b += state.step
    print("n={:<#10f} m={:<#10f} d={:<#10f} b={:<#10f}".format(n, m, delay, b))

    pixels.brightness = b
    return after(delay, main)

after(0, reset)
after(0, main)
start()