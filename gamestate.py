import pygame
import sys
import random
from mob import Mob
from cards import *
from sounds import *

WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

card_types = [AttackCard1, DefendCard1, AttackCard1, DefendCard1, AttackCard1]

class PoisonLogo(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frame_width, frame_height, num_frames, position, target_width, target_height):
        super().__init__()
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.5  # Adjust this value to control the animation speed
        self.animation_counter = 0
        self.position = position
        self.target_width = target_width
        self.target_height = target_height
        
        self.extract_frames()
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def extract_frames(self):
        for i in range(self.num_frames):
            frame = self.sprite_sheet.subsurface(
                (i * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            resized_frame = pygame.transform.scale(frame, (self.target_width, self.target_height))
            self.frames.append(resized_frame)

    def update(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.image = self.frames[self.current_frame]

class VulnerableLogo(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, frame_width, frame_height, num_frames, position, target_width, target_height):
        super().__init__()
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.frames = []
        self.current_frame = 0
        self.animation_speed = 0.5  # Adjust this value to control the animation speed
        self.animation_counter = 0
        self.position = position
        self.target_width = target_width
        self.target_height = target_height
        
        self.extract_frames()
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position

    def extract_frames(self):
        for i in range(self.num_frames):
            frame = self.sprite_sheet.subsurface(
                (i * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            resized_frame = pygame.transform.scale(frame, (self.target_width, self.target_height))
            self.frames.append(resized_frame)

    def update(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.image = self.frames[self.current_frame]

class GameState:
    def __init__(self, cards, dropbox, adventurer, mobs, font, energy_bar, all_sprites):
        self.cards = cards
        self.dropbox = dropbox
        self.adventurer = adventurer
        self.mobs = mobs
        self.state = "Start"
        self.clicked_card = None
        self.drag_offset = (0, 0)
        self.font = font
        self.choose_target_text = None
        self.energy_bar = energy_bar
        self.message = None
        self.message_time = 0
        self.turn_count = 0
        self.poison_count = 0
        self.vulnerable_count = 0
        self.poison_logo = None
        self.vulnerable_logo = None
        self.turn = "Adventurer"
        self.all_sprites = all_sprites  # Store all_sprites as an attribute
        self.game_over = False
        self.discard_pile = []
        self.original_card_types = [AttackCard1, DefendCard1, AttackCard1, DefendCard1, AttackCard1]
            
    def display_message(self, screen, message, duration):
        self.message = message
        self.message_time = pygame.time.get_ticks() + duration

    def draw_message(self, screen):
        if self.message and pygame.time.get_ticks() < self.message_time:
            message_surface = self.font.render(self.message, True, RED)
            message_rect = message_surface.get_rect(center=(screen.get_width() // 2, 50))
            screen.blit(message_surface, message_rect)
        else:
            self.message = None

    def draw_turn_count(self, screen):
        debug_font = pygame.font.Font(None, 36)
        turn_count_surface = debug_font.render(f"Turn: {self.turn_count}", True, WHITE)
        screen.blit(turn_count_surface, (10, 40))

    def handle_event(self, event, screen):
        if self.turn == "Adventurer":
            self.handle_adventurer_turn(event, screen)
        elif self.turn == "Mobs":
            self.handle_mob_turn()

    def handle_adventurer_turn(self, event, screen):
        for mob in self.mobs:
            if mob.current_hp <= 0:
                if mob.death():  # Call death() and check if it returns a value indicating it's finished
                    self.mobs.remove(mob)
                # Remove poison logo if exists
                    if hasattr(mob, 'poison_logo') and mob.poison_logo:
                        self.all_sprites.remove(mob.poison_logo)
                        mob.poison_logo = None

                    # Remove vulnerable logo if exists
                    if hasattr(mob, 'vulnerable_logo') and mob.vulnerable_logo:
                        self.all_sprites.remove(mob.vulnerable_logo)
                        mob.vulnerable_logo = None

                    mob.kill()
                    break       
            
        if self.state == "Start":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for card in self.cards:
                        if card.rect.collidepoint(event.pos):
                            self.clicked_card = card
                            self.drag_offset = (event.pos[0] - card.rect.x, event.pos[1] - card.rect.y)
                            self.state = "Clicked"
                            break
                elif event.button == 3:
                    for card in self.cards:
                        if card.rect.collidepoint(event.pos):
                            self.clicked_card = card
                            self.state = "Info"
                            break
                if self.clicked_card:
                    self.clicked_card.image = self.clicked_card.original_image
        elif self.state == "Clicked":
            if event.type == pygame.MOUSEMOTION:
                self.state = "Dragged"
            else:
                self.state = "Start"
                self.clicked_card = None
        elif self.state == "Info":
            if self.clicked_card:
                self.clicked_card.rect.y = 290
                self.clicked_card.image = pygame.transform.smoothscale(self.clicked_card.image, (380, 532))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.state = "Clicked"
                        self.clicked_card.image = self.clicked_card.original_image
                    elif event.button == 3:
                        self.state = "Start"
                        self.clicked_card.rect.topleft = self.clicked_card.original_pos
                        self.clicked_card.image = self.clicked_card.original_image
                        self.clicked_card = None
        elif self.state == "Target":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_mob = None
                    for mob in self.mobs:
                        if mob.rect.collidepoint(event.pos):
                            clicked_mob = mob
                            break
                    if clicked_mob:
                        if isinstance(self.clicked_card, AttackCard1):
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                if clicked_mob.vulnerable_counter > 0:
                                    # Apply vulnerability damage bonus
                                    damage = int(self.clicked_card.damage * 1.5)
                                else:
                                    damage = self.clicked_card.damage
                                clicked_mob.current_hp -= damage
                                self.adventurer.attack_animation()
                                if self.clicked_card in self.cards:
                                    self.cards.remove(self.clicked_card)
                                    self.energy_bar.update_energy(-self.clicked_card.energy_cost)
                                attack_card1_sfx.play()
                            else:
                                self.display_message(screen, "Not enough energy", 1000)
                        elif isinstance(self.clicked_card, AttackCard3): 
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                if clicked_mob.vulnerable_counter > 0:
                                    # Apply vulnerability damage bonus
                                    damage = int(self.clicked_card.damage * 1.5)
                                else:
                                    damage = self.clicked_card.damage
                                clicked_mob.current_hp -= damage
                                clicked_mob.poison_counter += 3  # Apply poison effect
                                self.adventurer.attack_animation()
                                if self.clicked_card in self.cards:
                                    self.cards.remove(self.clicked_card)
                                    self.energy_bar.update_energy(-self.clicked_card.energy_cost)
                                self.poison_logo = PoisonLogo('Sprites/poison.png', 24, 24, 8, (mob.rect.x, mob.rect.y - 120), 70, 70)  # Assign poison_logo
                                self.all_sprites.add(self.poison_logo)
                                clicked_mob.poison_logo = self.poison_logo
                                attack_card3_sfx.play()
                            else:
                                self.display_message(screen, "Not enough energy", 1000)
                        elif isinstance(self.clicked_card, AttackCard5):
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                if clicked_mob.vulnerable_counter > 0:
                                    # Apply vulnerability damage bonus
                                    damage = int(self.clicked_card.damage * 1.5)
                                else:
                                    damage = self.clicked_card.damage
                                clicked_mob.current_hp -= damage
                                self.adventurer.attack_animation()
                                clicked_mob.vulnerable_counter += 2
                                clicked_mob.vulnerable_turns = 2
                                if self.clicked_card in self.cards:
                                    self.cards.remove(self.clicked_card)
                                    self.energy_bar.update_energy(-self.clicked_card.energy_cost)
                                self.vulnerable_logo = VulnerableLogo('Sprites/vulnerable.png', 93, 84, 7, (mob.rect.x + 70, mob.rect.y - 120), 70, 70)  # Assign vulnerable
                                self.all_sprites.add(self.vulnerable_logo)
                                clicked_mob.vulnerable_logo = self.vulnerable_logo
                                attack_card5_sfx.play()
                            else:
                                self.display_message(screen, "Not enough energy", 1000)
                        elif isinstance(self.clicked_card, AttackCard6):
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                if clicked_mob.vulnerable_counter > 0:
                                    # Apply vulnerability damage bonus
                                    damage = int(self.clicked_card.damage * 1.5)
                                else:
                                    damage = self.clicked_card.damage
                                clicked_mob.current_hp -= damage
                                self.adventurer.attack_animation()
                                if self.clicked_card in self.cards:
                                    self.cards.remove(self.clicked_card)
                                    self.energy_bar.update_energy(-self.clicked_card.energy_cost)
                                    attack_card6_sfx.play()
                            else:
                                self.display_message(screen, "Not enough energy", 1000)
                        self.state = "Start"
                        self.clicked_card = None
                        self.choose_target_text = None

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.clicked_card:
                    if self.dropbox.is_inside(event.pos):
                        if isinstance(self.clicked_card, AttackCard1):
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                self.state = "Target"
                                self.choose_target_text = "Choose Target"
                                self.clicked_card.kill()
                                self.discard_pile.append(type(self.clicked_card))
                            else:
                                self.display_message(screen, "Not enough energy", 1000)
                                self.clicked_card.rect.topleft = self.clicked_card.original_pos
                        elif isinstance(self.clicked_card, DefendCard1):
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                self.adventurer.current_health += self.clicked_card.shield
                                self.cards.remove(self.clicked_card)
                                self.clicked_card.kill()
                                self.adventurer.shield_animation()
                                self.energy_bar.update_energy(-self.clicked_card.energy_cost)
                                self.discard_pile.append(type(self.clicked_card))
                                defend_card1_sfx.play()
                            else:
                                self.display_message(screen, "Not enough energy", 1000)
                                self.clicked_card.rect.topleft = self.clicked_card.original_pos
                        elif isinstance(self.clicked_card, AttackCard2):
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                for mob in self.mobs:
                                    if mob.vulnerable_counter > 0:
                                         # Apply vulnerability damage bonus
                                        damage = int(self.clicked_card.damage * 1.5)
                                    else:
                                        damage = self.clicked_card.damage
                                    mob.current_hp -= damage
                                self.cards.remove(self.clicked_card)
                                self.clicked_card.kill()
                                self.adventurer.attack_animation()
                                self.energy_bar.update_energy(-self.clicked_card.energy_cost)
                                self.discard_pile.append(type(self.clicked_card))
                                attack_card2_sfx.play()
                            else:
                                self.display_message(screen, "Not enough energy", 1000)
                                self.clicked_card.rect.topleft = self.clicked_card.original_pos
                        elif isinstance(self.clicked_card, AttackCard3): 
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                self.state = "Target"
                                self.choose_target_text = "Choose Target"
                                self.clicked_card.kill()
                                self.discard_pile.append(type(self.clicked_card))
                            else:
                                    self.display_message(screen, "Not enough energy", 1000)
                                    self.clicked_card.rect.topleft = self.clicked_card.original_pos
                        elif isinstance(self.clicked_card, AttackCard4):
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                for mob in self.mobs:
                                    if mob.vulnerable_counter > 0:
                                        # Apply vulnerability damage bonus
                                        damage = int(self.clicked_card.damage * 1.5)
                                    else:
                                        damage = self.clicked_card.damage
                                    mob.current_hp -= damage
                                self.adventurer.current_health -= self.clicked_card.health
                                self.cards.remove(self.clicked_card)
                                self.clicked_card.kill()
                                self.adventurer.attack_animation()
                                self.energy_bar.update_energy(-self.clicked_card.energy_cost)
                                self.discard_pile.append(type(self.clicked_card))
                            else:
                                self.display_message(screen, "Not enough energy", 1000)
                                self.clicked_card.rect.topleft = self.clicked_card.original_pos
                        elif isinstance(self.clicked_card, AttackCard5):
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                self.state = "Target"
                                self.choose_target_text = "Choose Target"
                                self.clicked_card.kill()
                                self.discard_pile.append(type(self.clicked_card))
                            else:
                                self.display_message(screen, "Not enough energy", 1000)
                                self.clicked_card.rect.topleft = self.clicked_card.original_pos
                        elif isinstance(self.clicked_card, AttackCard6):
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                self.state = "Target"
                                self.choose_target_text = "Choose Target"
                                self.clicked_card.kill()
                                self.discard_pile.append(type(self.clicked_card))
                            else:
                                self.display_message(screen, "Not enough energy", 1000)
                                self.clicked_card.rect.topleft = self.clicked_card.original_pos
                        elif isinstance(self.clicked_card, DefendCard2):
                            if self.energy_bar.current_energy >= self.clicked_card.energy_cost:
                                self.adventurer.current_health += self.clicked_card.shield
                                self.cards.remove(self.clicked_card)
                                self.clicked_card.kill()
                                self.adventurer.shield_animation()
                                self.energy_bar.update_energy(-self.clicked_card.energy_cost)
                                self.discard_pile.append(type(self.clicked_card))
                                self.reshuffle()
                                defend_card2_sfx.play()
                            else:
                                self.display_message(screen, "Not enough energy", 1000)
                                self.clicked_card.rect.topleft = self.clicked_card.original_pos
                    else:
                        self.clicked_card.rect.topleft = self.clicked_card.original_pos
                    if self.state == "Dragged":
                        self.state = "Start"
                        self.clicked_card = None
        elif event.type == pygame.MOUSEMOTION:
            if self.clicked_card and self.state == "Dragged":
                self.clicked_card.rect.x = event.pos[0] - self.drag_offset[0]
                self.clicked_card.rect.y = event.pos[1] - self.drag_offset[1]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def handle_mob_turn(self):
        for mob in self.mobs:
            if mob.current_hp > 0:
                mob.handle_behavior(self.adventurer)
                mob.apply_poison_damage()

                if mob.vulnerable_counter > 0:
                    mob.vulnerable_turns -= 1
                    if mob.vulnerable_turns <= 0:
                        mob.vulnerable_counter = 0
                        # Remove vulnerable logo if exists
                        if hasattr(mob, 'vulnerable_logo') and mob.vulnerable_logo:
                            self.all_sprites.remove(mob.vulnerable_logo)
                            mob.vulnerable_logo = None

            if self.adventurer.current_health <= 0:
                self.adventurer.death_animation()
                die_sound.play()
                self.game_over = True

        self.turn_count += 1
        print(self.poison_count)

        self.turn = "Adventurer"
        self.refill_cards()
        
    def end_adventurer_turn(self):
        self.turn = "Mobs"

    def shuffle_hand(self):
        if len(self.cards) == 5:
            random.shuffle(self.cards)

    def reshuffle(self):
        card_positions = [(350 + i * 250, 800) for i in range(5)]

        # Move all cards from hand and discard pile to card_types
        for card in self.cards:
            self.all_sprites.remove(card)
            card_types.append(type(card))  # Add the card type to card_types
        self.cards.clear()

        for discarded_card in self.discard_pile:
            card_types.append(discarded_card)
        self.discard_pile.clear()

        # Refill the hand with 5 random cards from card_types
        for _ in range(5):
            if card_types:
                card_type = random.choice(card_types)
                pos = card_positions[len(self.cards)]
                card = card_type(pos)
                self.cards.append(card)
                self.all_sprites.add(card)
                card_types.remove(card_type)

        # Ensure each card is in its designated position
        for i, card in enumerate(self.cards):
            card.rect.topleft = card_positions[i]
            card.original_pos = card_positions[i]

        if self.game_over:
            card_types.clear()
            card_types.extend(self.original_card_types)

    def refill_cards(self):
        card_positions = [(350 + i * 250, 800) for i in range(5)]

######################
        print("Before refill:")
        print("Card Types:", card_types)
        print("Discard Pile:", self.discard_pile)
        print("Hand:", self.cards)
######################

        # Shuffle the card types
        random.shuffle(card_types)
                        
        # Refill the hand with 5 cards, ensuring no duplicates initially
        while len(self.cards) < 5:
            if not card_types:
                # Refill card_types from discard_pile if it's empty
                card_types.extend(self.discard_pile)
                random.shuffle(card_types)
                self.discard_pile.clear()
                if not card_types:
                    break

            # Pop a card type from card_types and create a card instance
            card_type = card_types.pop()
            card = card_type(card_positions[len(self.cards)])
            self.cards.append(card)
            self.all_sprites.add(card)

        # Ensure each card is in its designated position
        for i, card in enumerate(self.cards):
            card.rect.topleft = card_positions[i]
            card.original_pos = card_positions[i]

        # Refill the energy bar to max
        self.energy_bar.current_energy = self.energy_bar.max_energy

#####################
        print("After refill:")
        print("Card Types:", card_types)
        print("Discard Pile:", self.discard_pile)
        print("Hand:", self.cards)
#####################

        # If the game is over, reset card_types to the original set of cards
        if self.game_over:
            card_types.clear()
            card_types.extend(self.original_card_types)

        return card_types

    def draw_debug_info(self, screen):
        if self.state == "Target" and self.choose_target_text:
            target_text_surface = self.font.render(self.choose_target_text, True, WHITE)
            screen.blit(target_text_surface, ((screen.get_width() - target_text_surface.get_width()) // 2, 20))

    def draw_end_turn_button(self, screen):
        pygame.draw.rect(screen, RED, self.end_turn_button_rect)
        button_text = self.font.render("End Turn", True, WHITE)
        button_rect = button_text.get_rect(center=self.end_turn_button_rect.center)
        screen.blit(button_text, button_rect)
        
def fade_to_black(screen):
    fade_surface = pygame.Surface((1920, 1080))
    fade_surface.set_alpha(0)  # Start with transparency
    for alpha in range(0, 256, 10):  # Increase alpha gradually
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))

        pygame.display.flip()
        pygame.time.delay(100)