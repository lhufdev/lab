import random

import pygame

from circleshape import CircleShape
from constants import ASTEROID_COL, ASTEROID_MIN_RADIUS, LINE_WIDTH
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, ASTEROID_COL, self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        velocity_a = self.velocity.rotate(+angle)
        velocity_b = self.velocity.rotate(-angle)
        radius = self.radius - ASTEROID_MIN_RADIUS

        new_asteroid_a = Asteroid(self.position.x, self.position.y, radius)
        new_asteroid_b = Asteroid(self.position.x, self.position.y, radius)

        new_asteroid_a.velocity = velocity_a * 1.2
        new_asteroid_b.velocity = velocity_b * 1.2
