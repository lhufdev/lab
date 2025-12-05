import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import (
    GAME_OVER_MESSAGE,
    PYGAME_VERSION,
    SCREEN_FILL_COL,
    SCREEN_FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    print(f"Starting Asteroids with pygame version: {PYGAME_VERSION}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # initialise pygame and create game window
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # setup the game clock and delta time
    clock = pygame.time.Clock()
    dt = 0

    # setup groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    # instantiate game objects
    _asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # main game loop
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill(SCREEN_FILL_COL)
        updatable.update(dt)

        # player-asteroid collision check
        for a in asteroids:
            if a.collides_with(player):
                log_event("player_hit")
                print(GAME_OVER_MESSAGE)
                sys.exit()

        # asteroid-shot collision check
        for a in asteroids:
            for s in shots:
                if s.collides_with(a):
                    log_event("asteroid_shot")
                    s.kill()
                    a.split()

        for d in drawable:
            d.draw(screen)

        pygame.display.flip()
        dt = clock.tick(SCREEN_FPS) / 1000


if __name__ == "__main__":
    main()
