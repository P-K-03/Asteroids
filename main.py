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
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)

    # Instantiate the player
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y, PLAYER_RADIUS)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

    clock = pygame.time.Clock()
    dt = 0
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        # Game
        screen.fill("black")
        
        for element in updatable:
            element.update(dt)
        
        # Collosion with players and bullets
        for asteroid in asteroids:
            if asteroid.isColliding(player):
                print("Game Over!")
                return
            for shot in shots:
                if shot.isColliding(asteroid):
                    shot.kill()
                    asteroid.split()

        for element in drawable:
            element.draw(screen)
            
        pygame.display.flip()
        dt = clock.tick(80)/1000 #Limiting the frame rate to 80 FPS


if __name__ == "__main__":
    main()