from particle import Particle
import random
import util
import math
import pygame

# The explosion itself
class Firework:
    def __init__(self, pos, colour, velocity, particleSize, sparsity, hasTrail, lifetime):
        # sparsity is between 0 and 1, higher values mean fewer particles
        trailColour = [random.uniform(0, 255),
                       random.uniform(0, 255),
                       random.uniform(0, 255)]
        xDir = -0.5
        while xDir <= 0.5:
            yDir = -0.5
            while yDir <= 0.5:
                if (xDir == yDir == 0):
                    continue
                if ( (xDir*xDir + yDir*yDir) <= 0.5*0.5):
                    Particle(pos=pos,
                             colour=colour,
                             direction=[xDir, yDir],
                             velocity=velocity + random.uniform(-2, 2),
                             size=particleSize,
                             hasTrail=hasTrail,
                             lifetime=lifetime + random.uniform(-3, 3),
                             shrink=True,
                             trailColour=trailColour)
                yDir += sparsity
            xDir += sparsity

# The little shooter that flies up and explodes
class Sparker:
    size = 3
    colour = [80, 20, 20]
    startVelocity = 100
    minVelocity = 0
    gravityPower = 5

    allSparkers = []

    def __init__(self, pos, colour, velocity, particleSize, sparsity, hasTrail, lifetime):
        # store firework attributes
        self.targetPos = pos
        self.colour = colour
        self.fwVelocity = velocity
        self.particleSize = particleSize
        self.sparsity = sparsity
        self.hasTrail = hasTrail
        self.fwLifetime = lifetime

        # setup sparker to fly in direction of cursor
        self.pos = [random.uniform(util.SCREEN_SIZE[0] * 1/3, util.SCREEN_SIZE[0] * 2/3),
                    util.SCREEN_SIZE[1]]
        rad = math.atan2(self.targetPos[1] - self.pos[1], self.targetPos[0] - self.pos[0])
        self.direction = [math.cos(rad), math.sin(rad)] # increase y a bit to offset gravity
        self.velocity = Sparker.startVelocity

        self.surface = pygame.Surface((Sparker.size, Sparker.size))
        self.surface.fill(Sparker.colour)

        Sparker.allSparkers.append(self)

    def update(self, dt):
        # move
        for axis in (0, 1):
            self.pos[axis] += self.direction[axis] * self.velocity * dt

        # gravity acts
        self.velocity -= Sparker.gravityPower * dt

        # if above target y or going slowly, time to detonate
        if self.pos[1] <= self.targetPos[1] or self.velocity < Sparker.minVelocity:
            self.detonate()

    def draw(self, screen):
        screen.blit(self.surface, self.pos)

    def detonate(self):
        Firework(self.pos, self.colour, self.fwVelocity, self.particleSize,
                 self.sparsity, self.hasTrail, self.fwLifetime)
        Sparker.allSparkers.remove(self)