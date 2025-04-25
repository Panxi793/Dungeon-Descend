import pygame

# Define card dimensions
CARD_WIDTH = 300
CARD_HEIGHT = 450

class Card(pygame.sprite.Sprite):
    def __init__(self, pos, image_path):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert()  # Load card image
        self.original_image = pygame.transform.scale(self.original_image, (CARD_WIDTH, CARD_HEIGHT))  # Scale image to card dimensions
        self.image = self.original_image.copy()  # Create a copy of the original image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.original_pos = pos  # Store original position
        self.damage = 0  # Default damage value
        self.shield = 0  # Default shield value

class AttackCard(Card):
    def __init__(self, pos, card_number):
        super().__init__(pos, f'Cards/Attack{card_number}.png')

class DefendCard(Card):
    def __init__(self, pos, card_number):
        super().__init__(pos, f'Cards/Defend{card_number}.png')

# Create subclasses for specific attack and defend cards
class AttackCard1(AttackCard):
    def __init__(self, pos):
        super().__init__(pos, 1) #attack
        self.damage = 5
        self.energy_cost = 1
        
class DefendCard1(DefendCard):
    def __init__(self, pos):
        super().__init__(pos, 1) #shield
        self.shield = 5
        self.energy_cost = 1

class AttackCard2(AttackCard):
    def __init__(self, pos):
        super().__init__(pos, 2) #slash
        self.damage = 2
        self.energy_cost = 1

class AttackCard3(AttackCard):
    def __init__(self, pos):
        super().__init__(pos, 3) #poison stab
        self.damage = 5
        self.energy_cost = 1

class AttackCard4(AttackCard):
    def __init__(self, pos):
        super().__init__(pos, 4) #havoc
        self.damage = 10
        self.energy_cost = 2
        self.health = 10

class AttackCard5(AttackCard):
    def __init__(self, pos):
        super().__init__(pos, 5) #heavy slash
        self.damage = 10
        self.energy_cost = 2
        #Add vulnerable

class AttackCard6(AttackCard):
    def __init__(self, pos):
        super().__init__(pos, 6) #die
        self.damage = 20
        self.energy_cost = 3

class DefendCard2(DefendCard):
    def __init__(self, pos):
        super().__init__(pos, 2) #acrobatics
        self.energy_cost = 0
