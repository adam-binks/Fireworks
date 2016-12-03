import pygame

pygame.init()

FULLSCREEN_MODE = True
if FULLSCREEN_MODE:
    screenInfo = pygame.display.Info()
    SCREEN_SIZE = [screenInfo.current_w, screenInfo.current_h]
else:
    SCREEN_SIZE = [1200, 800]

def isOnScreen(pos):
    for axis in (0, 1):
        if pos[axis] < 0 or pos[axis] > SCREEN_SIZE[axis]:
            return False
    return True