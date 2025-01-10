import pygame
import random
from circleshape import *
from constants import *
class Asteroid(CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def kill_asteroid(self):
        self.kill()
    
    def split(self):
        # Kill the asteroid
        self.kill_asteroid()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        # if asteroids are big or medium, split them
        else:
            random_angle = random.uniform(20, 50)
            vector_1 = self.velocity.rotate(random_angle)
            vector_2 = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            debris_1 = Asteroid(self.position.x , self.position.y, new_radius)
            debris_2 = Asteroid(self.position.x , self.position.y, new_radius)
            debris_1.velocity = vector_1 * 1.2
            debris_2.velocity = vector_2 * 1.2





    

