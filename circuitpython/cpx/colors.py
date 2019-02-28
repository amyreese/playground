RED = (255, 0, 0)
ORANGE = (255, 100, 0)
YELLOW = (255, 255, 0)
LIME = (150, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 150)
BLUE = (0, 0, 255)
INDIGO = (100, 0, 255)
VIOLET = (255, 0, 255)
WHITE = (200, 200, 200)
OFF = (0,0,0)

RAINBOW = (RED, ORANGE, YELLOW, LIME, GREEN, CYAN, BLUE, INDIGO, VIOLET)
ALL = RAINBOW + (WHITE, )

def cycle(colors=RAINBOW):
    while True:
        for color in colors:
            yield color
