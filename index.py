import pygame
import sys
import random

from particle import Particle
from spawner import Sparker
import util

FPS = 144  # can change this to 60 depending on your monitor refresh rate
FADE_RATE = 2 # lower values mean fireworks fade out more slowly

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
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            Sparker(pos=list(pygame.mouse.get_pos()),
                    colour=[random.uniform(0, 255),
                            random.uniform(0, 255),
                            random.uniform(0, 255)],
                    velocity=random.uniform(40, 60),
                    particleSize=10, sparsity=random.uniform(0.05, 0.15),
                    hasTrail=random.uniform(0, 1) < 0.3,
                    lifetime=random.uniform(10, 20),
                    )

def main():
    pygame.init()
    runGame()


if __name__ == '__main__':
    main()
