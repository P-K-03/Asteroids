# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import * 
from player import *
from asteroid import *
from asteroidfield import * 

def main():
    print("Starting asteroids!")
    pygame.init()

    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)

    # Instantiate the player
    player = Player(x, y, PLAYER_RADIUS)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            


        screen.fill("black")
        for elements in drawable:
            elements.draw(screen)
        
        for elements in updatable:
            elements.update(dt)
        # player.draw(screen)
        # player.update(dt)
        pygame.display.flip()
        dt = clock.tick(100)/1000


if __name__ == "__main__":
    main()