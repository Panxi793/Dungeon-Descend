import pygame
import sys
import cards  
from gamestate import *
from sounds import *

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define card dimensions
CARD_WIDTH = 300
CARD_HEIGHT = 450

class FloorCardList:
    def __init__(self):
        self.floor_cards = {
            1: [cards.AttackCard2, cards.DefendCard1],
            2: [cards.AttackCard3, cards.AttackCard2],
            3: [cards.AttackCard2, cards.AttackCard3],
            4: [cards.AttackCard4, cards.DefendCard2],
            5: [cards.DefendCard2, cards.AttackCard4],
            6: [cards.DefendCard1, cards.AttackCard5],
            7: [cards.AttackCard5, cards.AttackCard6],
            8: [cards.AttackCard6, cards.AttackCard5],
            9: [cards.AttackCard4, cards.AttackCard5],
        }

    def get_floor_cards(self, floor_number):
        return self.floor_cards.get(floor_number, [])

# Instantiate the FloorCardList class
floor_card_manager = FloorCardList()

def show_reward_screen(floor_number, card_types, game_state):
    pygame.init()

    display_width = 1920
    display_height = 1080

    screen = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Dungeon Descent')

    bg_music.stop()
    # Load the background image
    background_image = pygame.image.load("Sprites/reward.png").convert_alpha()
    background_image = pygame.transform.scale(background_image, (display_width, display_height))

    custom_font_path = "Scripts/PressStart2P-Regular.ttf"  # Path to the custom font file
    font_size1 = 38  # Increased font size for text1
    font_size2 = 28  # Font size for text2 remains the same
    font1 = pygame.font.Font(custom_font_path, font_size1)  # Using the larger font size for text1
    font2 = pygame.font.Font(custom_font_path, font_size2)  # Using the regular font size for text2

    reward_text1 = "Congratulations! You've defeated all the mobs!"
    reward_text2 = "Choose a Card:"
    text_surface1 = font1.render(reward_text1, True, WHITE)
    text_surface2 = font2.render(reward_text2, True, WHITE)

    text_rect1 = text_surface1.get_rect(center=(display_width // 2, 100))
    text_rect2 = text_surface2.get_rect(center=(display_width // 2, 300))

    clock = pygame.time.Clock()

    running = True
    card_instances = []  # List to store card instances

    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for card in card_instances:
                    if card.rect.collidepoint(mouse_pos):
                        card_types.append(card.__class__)
                        print(f"Selected card: {card}")
                        pick_card.play()
                        running = False  # Exit the loop
                        break

        # Blit the background image onto the screen
        screen.blit(background_image, (0, 0))
        screen.blit(text_surface1, text_rect1)
        screen.blit(text_surface2, text_rect2)
    
        card_width = CARD_WIDTH
        card_height = CARD_HEIGHT
        x_start = 540
        y = 400
        spacing = 200

        card_list = floor_card_manager.get_floor_cards(floor_number)
        for i, card_type in enumerate(card_list):
            x = x_start + i * (card_width + spacing)
            card = card_type((x, y))  # Create an instance of the card type
            card_image = pygame.transform.scale(card.original_image, (card_width, card_height))
            screen.blit(card_image, card.rect)
            card_instances.append(card)  # Store card instance

        pygame.display.flip()
        clock.tick(60)
    
    for card in game_state.cards:
        card_types.append(type(card))
    for card in game_state.discard_pile:
        card_types.append(card)
    
    return card_types

