# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import * 
from player import *

def main():
    print("Starting asteroids!")
    pygame.init()
# Instantiate the player
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y, PLAYER_RADIUS)

    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    while(True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        player.draw(screen)
        pygame.display.flip()
        dt = clock.tick(100)/1000


if __name__ == "__main__":
    main()