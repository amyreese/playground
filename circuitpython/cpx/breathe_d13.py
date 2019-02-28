import board
import pulseio

from colors import RAINBOW, BLUE, YELLOW, WHITE
from cpgame import every, tick, start

STEP = 40
UPPER = (2 ** 15) - STEP
LOWER = 2 ** 9
START = LOWER

pwm = pulseio.PWMOut(
    board.D13, duty_cycle=START, frequency=800
)

class state:
    step = STEP

@tick
def main(now):
    if pwm.duty_cycle >= UPPER and state.step > 0:
        state.step = -state.step
    if pwm.duty_cycle <= LOWER and state.step < 0:
        state.step = -state.step
    
    pwm.duty_cycle += state.step
    print(pwm.duty_cycle)

start()