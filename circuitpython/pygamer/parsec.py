import board
import neopixel
import random

from colors import RED, GREEN, BLUE

from cpgame import (
    start, after, every, on, sample, enable_speaker, play_sound,
    DIGITALIO, TOUCHIO, GAMEPAD
)

SOUNDS = {
    "blue": sample(659),  # E
    "green": sample(329),  # Low E
    "red": sample(440),  # A
    "yellow": sample(554),  # C#
}
NAMES = list(SOUNDS.keys())

pixels = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness=0.05, auto_write=False)
pixels.fill(BLUE)
pixels.show()

@every(7)
def loop(now):
    name = random.choice(NAMES)
    sound = SOUNDS[name]
    play_sound(sound, 0.1)
    print(name)

for pin in TOUCHIO:
    break
    try:
        @on(pin)
        def pressed(now):
            print("pressed " + str(pin) + " at " + str(now))

    except Exception as e:
        print(e)

@on(GAMEPAD.A)
def pressed(now):
    print("A pressed")


# enable_speaker()
start()