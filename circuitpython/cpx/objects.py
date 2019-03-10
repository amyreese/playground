from sys import stdin, stdout
from time import sleep

import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull 
from supervisor import runtime

from cpgame import after, cancel, every, on, start
from colors import RED, ORANGE, GREEN, YELLOW, BLUE, VIOLET, WHITE, OFF

pixels = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.02, auto_write=True)
pixels.fill(OFF)
pixels.show()

WAIT = DigitalInOut(board.D7)
WAIT.direction = Direction.INPUT
WAIT.pull = Pull.UP

LED = DigitalInOut(board.D13)
LED.direction = Direction.OUTPUT

STATUS = 9

class state:
    active = 0
    handshake = 0
    data = ""


def send(cmd):
    if cmd.endswith("\n"):
        line = cmd
    else:
        line = cmd + "\n"
    stdout.write(line)
    old = pixels[STATUS]
    pixels[STATUS] = YELLOW
    sleep(0.05)
    pixels[STATUS] = old


def sync(now):
    send("DBG=Testing debug!")

    send("CMD=TOGGLE_MAIN_ENGINE,1")
    send("CMD=FULL_STOP,2")

    send("NIB=EMCON_MODE,1")
    send("NIB=IFF_ACTIVE,2")
    send("NIB=MAIN_ENGINE_BURNING,3")
    send("ACT")

    #on(board.D4, burn)
    #on(board.D5, stop)
    state.active = True


@every(3)
def handshake(now):
    if not state.handshake:
        send("451")


@every(0.1)
def loop(now):
    if state.active:
        pixels[STATUS] = GREEN
    elif state.handshake:
        pixels[STATUS] = YELLOW
    else:
        pixels[STATUS] = RED

    line = ""
    while runtime.serial_bytes_available:
        char = stdin.read(1)

        if char == "\r":
            pass
        elif char == "\n":
            line = state.data.strip()
            state.data = ""
        else:
            state.data += char

    if line == "452" and not state.handshake:
        state.handshake = True
        sync(now)
    elif line:
        try:
            key, value = line.split("=")
            # print("DBG=Got line {} -> key={}, value={}".format(line, key, value))
            key = (int(key) - 1) % STATUS
            value = int(value)
            pixels[key] = WHITE if value else OFF
        except Exception as e:
            # print("DBG=Got exception: {}".format(e))
            pass


@on(board.D4, board.D5)
def reset(now):
    state.data = ""
    state.active = False
    state.handshake = False
    pixels.fill(OFF)

        
@on(board.D4)
def burn(now):
    if state.active:
        send("EXC=1")


@on(board.D5)
def stop(now):
    if state.active:
        send("EXC=2")


start()