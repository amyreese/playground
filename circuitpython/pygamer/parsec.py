import board
import neopixel

from colors import RED, GREEN, BLUE

from cpgame import start, after, every, on, DIGITALIO, TOUCHIO

pixels = neopixel.NeoPixel(board.NEOPIXEL, 5, brightness=0.05, auto_write=False)
pixels.fill(BLUE)
pixels.show()

@every(1)
def loop(now):
    print(now)

for pin in TOUCHIO:
    try:
        @on(pin)
        def pressed(now):
            print("pressed " + str(pin) + " at " + str(now))

    except Exception as e:
        print(e)

start()