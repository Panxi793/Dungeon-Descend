import pygame

# Initialize the mixer module
pygame.mixer.init()

#Attack
attack_card1_sfx = pygame.mixer.Sound('Audio/attack.wav')
attack_card2_sfx = pygame.mixer.Sound('Audio/slash.mp3')
attack_card3_sfx = pygame.mixer.Sound('Audio/poison-stab.wav')
attack_card4_sfx = pygame.mixer.Sound('Audio/havoc.mp3')
attack_card5_sfx = pygame.mixer.Sound('Audio/heavy-slash.mp3')
attack_card6_sfx = pygame.mixer.Sound('Audio/die.wav')

#Defend
defend_card1_sfx = pygame.mixer.Sound('Audio/shield.wav')
defend_card2_sfx = pygame.mixer.Sound('Audio/acrobatics.mp3')
defend_card3_sfx = pygame.mixer.Sound('Audio/battle-cry.wav')

#Start
bg_music_start = pygame.mixer.Sound('Audio/bg-start.mp3')
run = pygame.mixer.Sound('Audio/run.mp3')

#Other
die_sound = pygame.mixer.Sound('Audio/dead.wav')
pick_card = pygame.mixer.Sound('Audio/pick_card.wav')
bg_music = pygame.mixer.Sound('Audio/bg-music.mp3')

# Export the sounds to be used in other modules
__all__ = ['bg_music', 'pick_card', 'die_sound', 'bg_music_start', 'run', 'attack_card1_sfx', 'defend_card1_sfx', 'defend_card2_sfx', 'defend_card3_sfx', 'attack_card2_sfx', 'attack_card3_sfx', 'attack_card4_sfx', 'attack_card5_sfx', 'attack_card6_sfx']  # Add all your sound variables here
