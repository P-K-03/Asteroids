# this allows us to use code from
# the open-source pygame library
# throughout this file
import sys

import pygame
import asyncio

from constants import * 
from player import *
from asteroid import *
from asteroidfield import * 

pygame.mixer.init()


def game_over_animation(screen, font, clock):
    """
    Clears the screen to black and displays "GAME OVER" with a letter-by-letter animation.
    The text will be centered on the screen.

    Behavior:
    - Pressing any key (except ESCAPE) during the letter animation will complete it instantly.
    - Pressing any key (except ESCAPE) after the text is fully displayed will exit this function.
    - Pressing ESCAPE at any time will quit the game.
    """
    screen_width, screen_height = screen.get_size()
    full_text_string = "GAME OVER"
    
    # --- Pre-calculate character surfaces and total text dimensions for centering ---
    char_surfaces = []  # List to hold rendered surfaces of individual characters
    char_widths = []    # List to hold widths of individual characters
    total_text_width = 0
    text_height = 0     # Max height of any character, effectively the line height

    # Render each character to get its dimensions
    for char_code in full_text_string:
        char_surface = font.render(char_code, True, "white") #--> FIX THIS
        char_surfaces.append(char_surface)
        
        char_width = char_surface.get_width()
        char_widths.append(char_width)
        total_text_width += char_width
        
        if char_surface.get_height() > text_height:
            text_height = char_surface.get_height()
            
    # Define spacing between letters (can be adjusted)
    # Making it dynamic based on font height for better scaling
    letter_spacing = max(1, font.get_height() // 10) 
    if len(full_text_string) > 1:
        total_text_width += letter_spacing * (len(full_text_string) - 1)

    # Calculate the starting X and Y coordinates for the entire text block to be centered
    start_x = (screen_width - total_text_width) // 2
    start_y = (screen_height - text_height) // 2

    # --- Animation variables ---
    displayed_char_count = 0  # How many characters are currently visible
    letter_appear_delay = 100 # Milliseconds between each letter appearing
    last_letter_time = pygame.time.get_ticks() # Time when the last letter was shown
    
    animating_letters = True  # True while letters are appearing one by one
    showing_full_text = False # True after all letters are visible (either by animation or skip)

    # Main loop for the animation and waiting phase
    while animating_letters or showing_full_text:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Always allow quitting with ESCAPE
                    pygame.quit()
                    sys.exit()
                
                if animating_letters and not showing_full_text:
                    # Key pressed during the letter-by-letter animation: complete it
                    displayed_char_count = len(full_text_string)
                    animating_letters = False # Stop letter-by-letter animation
                    showing_full_text = True  # Move to showing the full text
                    # The loop will continue, and the full text will be drawn in this iteration
                elif showing_full_text:
                    # Key pressed after the text is fully displayed: exit the function
                    showing_full_text = False # This will make the main while-loop condition false
                                            # and the function will return.

        # --- Logic for letter-by-letter appearance ---
        if animating_letters and not showing_full_text:
            current_time = pygame.time.get_ticks()
            if displayed_char_count < len(full_text_string):
                if current_time - last_letter_time > letter_appear_delay:
                    displayed_char_count += 1
                    last_letter_time = current_time
            else:
                # All letters have appeared naturally
                animating_letters = False
                showing_full_text = True
        
        # --- Drawing phase ---
        screen.fill("black") # Clear screen to black
        current_render_x = start_x # X position for the current character being drawn
        
        # Draw the characters that are currently meant to be visible
        chars_to_draw_now = displayed_char_count
        
        for i in range(chars_to_draw_now):
            if i < len(char_surfaces): # Safety check
                screen.blit(char_surfaces[i], (current_render_x, start_y))
                current_render_x += char_widths[i] + letter_spacing # Move to next char position
            
        pygame.display.flip() # Update the full screen
        clock.tick(60) # Maintain a consistent frame rate

    # Loop has exited, meaning the animation is done and a key was pressed to continue.


async def play_sound(loc : str, volume : float = 0.8 ): 
    pygame.mixer.music.load(loc)
    pygame.mixer.music.play(loops = 1)



async def main():
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
                font = pygame.font.SysFont("Arial", 80)
                await play_sound('tracks/game-over.mp3')
                game_over_animation(screen, font, clock)

                print("Game Over!")

                return
            
            for shot in shots:
                if shot.isColliding(asteroid):
                    radius = asteroid.radius
                    shot.kill()
                    await play_sound('tracks/asteroid-destruction.wav')
                    asteroid.split()

        for element in drawable:
            element.draw(screen)
            
        pygame.display.flip()
        dt = clock.tick(100)/1000 #Limiting the frame rate to 80 FPS


if __name__ == "__main__":
    asyncio.run(main())
