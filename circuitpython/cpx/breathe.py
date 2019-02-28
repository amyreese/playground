import board
import neopixel

from colors import RAINBOW, BLUE, YELLOW, WHITE
from cpgame import every, tick, start

STEP = 1.0 / 256
UPPER = STEP * 10
LOWER = STEP
START = LOWER

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=START)
pixels.fill(WHITE)

class state:
    value = START
    step = STEP

@every(0.15)
def main(now):
    if pixels.brightness >= UPPER and state.step > 0:
        state.step = -state.step
    if pixels.brightness <= LOWER and state.step < 0:
        state.step = -state.step
    
    pixels.brightness += state.step
    print(pixels.brightness)

start()