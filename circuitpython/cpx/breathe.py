import board
import neopixel

from colors import RAINBOW, BLUE, YELLOW, WHITE
from cpgame import every, tick, start

STEP = 1.0 / 256
UPPER = STEP * 30
LOWER = STEP * 2
START = LOWER

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=START)
pixels.fill(BLUE)
pixels[3], pixels[4], pixels[8], pixels[9] = YELLOW, YELLOW, YELLOW, YELLOW

class state:
    value = START
    step = STEP

@every(0.05)
def main(now):
    if pixels.brightness >= UPPER and state.step > 0:
        state.step = -state.step
    if pixels.brightness <= LOWER and state.step < 0:
        state.step = -state.step
    
    pixels.brightness += state.step
    print(pixels.brightness)

start()