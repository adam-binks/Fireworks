import pygame
import sys
import random
import math

from particle import Particle
from sparker import Sparker
import util

FPS = 600  # can lower this to reduce system resource usage
FADE_RATE = 2 # lower values mean fireworks fade out more slowly

# controls
FIREWORK_MOUSE_BUTTON = 1  # left click
SHIMMER_MOUSE_BUTTON = 3   # right click

# colours
BLACK = [0, 0, 0]
BLACK_FADED = [0, 0, 0, FADE_RATE]


def runGame():
    FPSClock = pygame.time.Clock()
    pygame.display.set_caption("Fireworks")

    if util.FULLSCREEN_MODE:
        screen = pygame.display.set_mode(util.SCREEN_SIZE, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(util.SCREEN_SIZE)

    # every frame blit a low alpha black surf so that all effects fade out slowly
    blackSurf = pygame.Surface(util.SCREEN_SIZE).convert_alpha()
    blackSurf.fill(BLACK_FADED)

    # GAME LOOP
    while 1:
        screen.blit(blackSurf, (0,0))
        dt = FPSClock.tick(FPS) / 60.0

        handleInput()

        for p in Particle.allParticles:
            p.update(dt)
            p.draw(screen)

        for s in Sparker.allSparkers:
            s.update(dt)
            s.draw(screen)

        screen.blit(screen, (0, 0))
        pygame.display.update()

        pygame.display.set_caption("Fireworks  (FPS " + str(round(FPSClock.get_fps(), 1)) + ")")

# click to spawn fireworks, escape to quit
def handleInput():
    for event in pygame.event.get():
        # terminate on system quit or esc key
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        # spawn fireworks on click
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == FIREWORK_MOUSE_BUTTON:
                Sparker(pos=list(pygame.mouse.get_pos()),
                        colour=[random.uniform(0, 255),
                                random.uniform(0, 255),
                                random.uniform(0, 255)],
                        velocity=random.uniform(40, 60),
                        particleSize=random.uniform(10, 20),
                        sparsity=random.uniform(0.05, 0.15),
                        hasTrail=True,
                        lifetime=random.uniform(10, 20),
                        isShimmer=False)

            if event.button == SHIMMER_MOUSE_BUTTON:
                Sparker(pos=list(pygame.mouse.get_pos()),
                        colour=[random.uniform(50, 255),
                                random.uniform(50, 255),
                                random.uniform(50, 255)],
                        velocity=random.uniform(1, 2),
                        particleSize=random.uniform(3, 8),
                        sparsity=random.uniform(0.05, 0.15),
                        hasTrail=False,
                        lifetime=random.uniform(20, 30),
                        isShimmer=True,
                        radius=random.uniform(40, 100),
                        proportion=0.6,
                        focusRad=random.choice([0, 0.4, 3, 6]),
                        weight=random.uniform(0.001, 0.0015))

def main():
    pygame.init()
    runGame()


if __name__ == '__main__':
    main()
