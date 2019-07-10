GAME_WIDTH = 1280
GAME_HEIGHT = 720

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

TOP_LEFT_X = 0
TOP_LEFT_Y = int((SCREEN_HEIGHT-GAME_HEIGHT)/2-5)

FULL_GAME = (TOP_LEFT_X, TOP_LEFT_Y, GAME_WIDTH, GAME_HEIGHT)

def g_to_s(pos):
    pos = list(pos)
    pos[0] += TOP_LEFT_X
    pos[1] += TOP_LEFT_Y
    return tuple(pos)