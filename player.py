import pygame
from circleshape import *
from shot import *
from constants import *

pygame.mixer.init()
class Player(CircleShape):
    
    def __init__(self, x, y, PLAYER_RADIUS):
        super().__init__(x,y,PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer  = 0

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "beige" , self.triangle(), 2)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
    
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        if self.shoot_timer > 0:
            return 
        else:
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN
            shot = Shot(self.position.x , self.position.y)
            shot.velocity = pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

        


    def update(self, dt):
        self.shoot_timer -= dt

        keys = pygame.key.get_pressed()
        

        if keys[pygame.K_a]:
            self.rotate(-dt)
            
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            pygame.mixer.music.load("tracks/shooting-laser.mp3")
            pygame.mixer.music.play(loops = 1)
            
            self.shoot()
            
        
