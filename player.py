# some of the code in this file was provided and *not* written by me

import pygame
from pygame.math import Vector2

from circleshape import CircleShape
from constants import (
    LINE_WIDTH,
    PLAYER_COL,
    PLAYER_RADIUS,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SHOT_RADIUS,
)
from shot import Shot


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self._shot_cooldown_timer = 0
        self.rotation = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, PLAYER_COL, self.triangle(), LINE_WIDTH)

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def shoot(self):
        shot = Shot(self.position[0], self.position[1], SHOT_RADIUS)
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        shot.velocity = rotated_vector * PLAYER_SHOOT_SPEED

    def update(self, dt):
        if self._shot_cooldown_timer > 0:
            self._shot_cooldown_timer -= dt

        keys = pygame.key.get_pressed()

        # player movement
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(+dt)
        if keys[pygame.K_w]:
            self.move(+dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        # player weapon controls
        if keys[pygame.K_SPACE]:
            if self._shot_cooldown_timer <= 0:
                self._shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
                self.shoot()
