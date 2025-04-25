import pygame
import sys
from main import *
from sounds import *

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize screen
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Main Menu")

# Load background image
background_image = pygame.image.load("Sprites/start.png")
background_image = pygame.transform.scale(background_image, SCREEN_SIZE)

# Load title image
title_image = pygame.image.load("Sprites/game_title.png")  # Replace "title.png" with your actual title image file
title_image = pygame.transform.scale(title_image, (1040, 340))  # Adjust size as needed

# Load sprite sheet for animation in main menu
sprite_sheet_idle = pygame.image.load("Sprites/idle_start.png")  # Load your main menu sprite sheet image here
sprite_width_idle = 280  # Adjust the sprite width as needed
sprite_height_idle = 350  # Adjust the sprite height as needed
num_frames_idle = 6  # Number of frames in the main menu sprite sheet
current_frame_idle = 0  # Index of the current frame in the main menu sprite sheet

# Load sprite sheet for animation in fade-to-black transition
sprite_sheet_run = pygame.image.load("Sprites/run_start.png")  # Load your fade-to-black sprite sheet image here
sprite_width_run = 360 # Adjust the sprite width as needed
sprite_height_run = 300  # Adjust the sprite height as needed
num_frames_run = 8  # Number of frames in the fade-to-black sprite sheet
current_frame_run = 0  # Index of the current frame in the fade-to-black sprite sheet

# Load custom font
custom_font = "Scripts/PressStart2P-Regular.ttf"

# Font
font = pygame.font.Font(custom_font, 36)

# Declare clock as a global variable
clock = pygame.time.Clock()

class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def main_menu():
    global current_frame_idle, current_frame_run, title_image  # Declare current_frame_idle and current_frame_run as global variables
    run_animation = False  # Initialize the flag to control the animation loop
    start_time = 0  # Variable to store the start time of the animation

    title_y = 70  # Initial y position of the title image
    move_direction = 'down'  # Flag to indicate the direction of movement

    bg_music_start.play(-1)
    
    while True:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        screen.blit(title_image, (SCREEN_WIDTH // 2 - title_image.get_width() // 2, title_y))
        
        # Move the title image
        if move_direction == 'down':
            title_y += 2  # Move down
            if title_y >= 85:  # If reached the lower limit
                move_direction = 'up'  # Change direction
        else:
            title_y -= 2  # Move up
            if title_y <= 70:  # If reached the upper limit
                move_direction = 'down'  # Change direction
        
        # Draw sprite sheet animation for main menu
        sprite_rect_idle = pygame.Rect(240, 520, sprite_width_idle, sprite_height_idle)
        screen.blit(sprite_sheet_idle, sprite_rect_idle, (current_frame_idle * sprite_width_idle, 0, sprite_width_idle, sprite_height_idle))
        
        # Update current frames for animations
        current_frame_idle = (current_frame_idle + 1) % num_frames_idle
        
        # Button initialization and event handling
        PLAY_BUTTON = Button(image=pygame.image.load("Sprites/button_rect.png"), pos=(960, 520), text_input="PLAY", font=pygame.font.Font(custom_font, 40), base_color="White", hovering_color="#d7fcd4")
        QUIT_BUTTON = Button(image=pygame.image.load("Sprites/button_rect.png"), pos=(960, 700), text_input="QUIT", font=pygame.font.Font(custom_font, 40), base_color="White", hovering_color="#d7fcd4")

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(pygame.mouse.get_pos())
            button.update(screen)

        # Handle button events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in [PLAY_BUTTON, QUIT_BUTTON]:
                    if button.checkForInput(pygame.mouse.get_pos()):
                        if button.text_input == "PLAY":
                            attack_card1_sfx.play()
                            bg_music_start.stop()
                            run.play()
                            run_animation = True  # Set the flag to start the animation
                            start_time = pygame.time.get_ticks()  # Record the start time of the animation
                        elif button.text_input == "QUIT":
                            attack_card1_sfx.play()
                            pygame.quit()
                            sys.exit()

        if run_animation:
            show_animation()  # Call the animation function if the flag is set
            elapsed_time = pygame.time.get_ticks() - start_time
            if elapsed_time > 3000:  # Check if 5 seconds have passed
                fade_to_black()
                main_game(1)
  
        pygame.display.flip()
        clock.tick(10)  # Control the frame rate

sprite_x = 250
def show_animation():
    global current_frame_run, sprite_x, animation_count  # Declare global variables
    
    animation_count = 0  # Initialize animation counter

    while animation_count < 4:  # Loop to repeat the animation 3 times
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        # Update sprite position
        sprite_x += 42  # Adjust the speed of movement as needed
        sprite_x %= SCREEN_WIDTH  # Wrap around the screen width

        # Draw sprite sheet animation for the show animation
        sprite_rect_run = pygame.Rect(sprite_x, 525, sprite_width_run, sprite_height_run)
        screen.blit(sprite_sheet_run, sprite_rect_run, (current_frame_run * sprite_width_run, 0, sprite_width_run, sprite_height_run))

        current_frame_run = (current_frame_run + 1) % num_frames_run

        pygame.display.flip()

        clock.tick(10)  # Control the frame rate

        # Check if the animation has completed 3 repetitions
        if current_frame_run == 0:  # Check if it's the first frame (start of new loop)
            animation_count += 1  # Increment animation counter   

    sprite_x = 250
def fade_to_black():
    global current_frame_idle, current_frame_run  # Declare current_frame_idle and current_frame_run as global variables
    
    fade_surface = pygame.Surface(SCREEN_SIZE)
    fade_surface.set_alpha(0)  # Start with transparency
    for alpha in range(0, 256, 10):  # Increase alpha gradually
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))

        pygame.display.flip()
        pygame.time.delay(100)  # Adjust the delay to control the speed of fade

if __name__ == "__main__":
    main_menu()
