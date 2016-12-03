import pygame
import util
import random

# hasTrail is whether this firework has the little different coloured trailer particles too
class Particle:
    gravityAmount = 0.005
    allParticles = []

    def __init__(self, pos, colour, direction, velocity, size, lifetime,
                 hasTrail=False, shrink=False,
                 trailColour=None, trailPercent=0.4):
        self.pos = [float(pos[0]), float(pos[1])]  # (x, y)
        self.colour = colour
        self.direction = direction  # (x movement, y movement)
        self.velocity = velocity
        self.size = size
        self.hasTrail = hasTrail
        self.lifetime = lifetime
        self.age = 0
        self.shrink = shrink

        self.surface = pygame.Surface((size, size))
        self.surface.fill(self.colour)

        Particle.allParticles.append(self)

        if hasTrail and random.uniform(0, 1) < trailPercent:
            self.spawnTrail(trailColour)

    def update(self, dt):
        # move
        for axis in (0, 1):
            self.pos[axis] += self.direction[axis] * self.velocity * dt

        # gravity acts
        self.direction[1] += Particle.gravityAmount * dt

        # check if needs to die (off screen or lifetime is over)
        self.age += dt
        if not util.isOnScreen(self.pos) or self.age > self.lifetime:
            self.die()
            return

        if self.shrink:
            newSurfSize = self.size*(1 - self.age/self.lifetime)
            self.surface = pygame.Surface((newSurfSize, newSurfSize))
            self.surface.fill(self.colour)

    def draw(self, screen):
        screen.blit(self.surface, self.pos)

    def die(self):
        if self in Particle.allParticles:
            Particle.allParticles.remove(self)

    def spawnTrail(self, trailColour):
        Particle(self.pos, trailColour, self.direction, self.velocity*2, self.size*0.25,
                 lifetime=self.lifetime*2.5)