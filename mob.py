import pygame
import random
import copy

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)

class Mob(pygame.sprite.Sprite):
    def __init__(self, name, max_hp, pos, id, at, de, sh):
        super().__init__()
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.animation_list = []
        self.frame_index = 0
        self.action = 0  # 0:idle, 1:attack, 2:dead, 3:shield
        self.update_time = pygame.time.get_ticks()
        self.id = id
        self.at = at
        self.de = de
        self.sh = sh
        self.vulnerable_counter = 0
        self.vulnerable_turns = 0
        self.poison_counter = 0
        self.poison_logo = None

        # load idle images
        temp_list = []
        for i in range(self.id):
            img = pygame.image.load(f'Sprites/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load attack images
        temp_list = []
        for i in range(self.at):
            img = pygame.image.load(f'Sprites/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load dead images
        temp_list = []
        for i in range(self.de):
            img = pygame.image.load(f'Sprites/{self.name}/Dead/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        # load shield images
        temp_list = []
        for i in range(self.sh):
            img = pygame.image.load(f'Sprites/{self.name}/Shield/{i}.png')
            img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
            temp_list.append(img)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.alive = True

    def apply_poison_damage(self):
        if self.poison_counter > 0:
            self.current_hp -= 3
            self.poison_counter -= 1
            if self.poison_counter == 0:
                self.remove_poison_logo()

    def remove_poison_logo(self):
        # Logic to remove the poison logo sprite if it exists
        if hasattr(self, 'poison_logo'):
            self.poison_logo.kill()

    def apply_vulnerability(self):
        if self.vulnerable_counter > 0:
            self.vulnerable_counter -= 1
            if self.vulnerable_counter == 0:
                self.remove_vulnerable_logo()

    def remove_vulnerable_logo(self):
        if hasattr(self, 'vulnerable_logo'):
            self.vulnerable_logo.kill()

    def update(self):
        animation_cooldown = 100
        # handle animation
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 2:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()

    def idle(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        damage = self.damage
        target.current_health -= damage

        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def apply_heal(self):
        heal_amount = self.heal
        self.current_hp += heal_amount

        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def death(self):
        if self.action != 2:  # Only reset the frame index when the death action starts
            self.action = 2
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        if self.frame_index < len(self.animation_list[self.action]) - 1:
            if pygame.time.get_ticks() - self.update_time > 100:  # Adjust the time delay as needed
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            return False  # Death animation is not finished
        return True  # Death animation is finished

    def draw(self, screen, font):
        custom_font = "Scripts/PressStart2P-Regular.ttf"
        font = pygame.font.Font(custom_font, 15)
        health_text = font.render(f"{self.name}: {self.current_hp}/{self.max_hp} HP", True, (255, 255, 255))
        health_text_rect = health_text.get_rect()
        health_text_rect.midtop = (self.rect.centerx, self.rect.y - 50)  # Position health text above health bar
        screen.blit(health_text, health_text_rect.topleft)
        screen.blit(self.image, self.rect)

    def draw_health_bar(self, screen):
        health_ratio = self.current_hp / self.max_hp
        health_ratio = min(health_ratio, 1.0)
        health_bar_width = self.rect.width // 1.75
        current_health_length = int(health_bar_width * health_ratio)
        
        # Calculate the x position to center the health bar above the sprite
        health_bar_x = self.rect.x + (self.rect.width - health_bar_width) // 2
        
        # Draw the background of the health bar (red)
        pygame.draw.rect(screen, RED, (health_bar_x, self.rect.y - 20, health_bar_width, 5))
        
        # Draw the current health (green)
        pygame.draw.rect(screen, GREEN, (health_bar_x, self.rect.y - 20, current_health_length, 5))
        
    def handle_behavior(self, adventurer):
        pass

class Slime(Mob):
    def __init__(self, pos):
        super().__init__("Slime", 5, pos, 8, 5, 3, 0)
        self.damage = 2

    def handle_behavior(self, adventurer):
        self.attack(adventurer)
        print(f"{self.name} attacks for {self.damage} damage!")

class Goblin(Mob):
    def __init__(self, pos):
        super().__init__("Goblin", 10, pos, 5, 4, 4, 7)
        self.damage = 3
        self.heal = 2

    def handle_behavior(self, adventurer):
        # Randomly choose between attacking and healing
        if random.choice([True, False]):
            # Attack behavior
            self.attack(adventurer)
            print(f"{self.name} attacks for {self.damage} damage!")
        else:
            # Heal behavior
            self.apply_heal()
            print(f"{self.name} heals for {self.heal} HP!")

class Spider(Mob):
    def __init__(self, pos):
        super().__init__("Spider", 10, pos, 9, 6, 4, 0)
        self.damage = 5
    
    def handle_behavior(self, adventurer):
        self.attack(adventurer)
        print(f"{self.name} attacks for {self.damage} damage!")

class Skeleton(Mob):
    def __init__(self, pos):
        super().__init__("Skeleton", 15, pos, 7, 4, 5, 1)
        self.damage = 7
        self.heal = 5

    def handle_behavior(self, adventurer):
        # Randomly choose between attacking and healing
        if random.choice([True, False]):
            self.attack(adventurer)
            print(f"{self.name} attacks for {self.damage} damage!")
        else:
            self.apply_heal()
            print(f"{self.name} heals for {self.heal} HP!")

class Golem(Mob):
    def __init__(self, pos):
        super().__init__("Golem", 30, pos, 4, 5, 4, 8)
        self.damage = 10
        self.heal = 5

    def handle_behavior(self, adventurer):
        if random.choice([True, False]):
            self.attack(adventurer)
            print(f"{self.name} attacks for {self.damage} damage!")
        else:
            self.apply_heal()
            print(f"{self.name} heals for {self.heal} HP!")

class Boss(Mob):
    def __init__(self, pos):
        super().__init__("Boss", 50, pos, 5, 5, 5, 2)
        self.damage = 12
        self.heal = 7

    def handle_behavior(self, adventurer):
        # Randomly choose between attacking and healing
        if random.choice([True, False]):
            self.attack(adventurer)
            print(f"{self.name} attacks for {self.damage} damage!")
        else:
            self.apply_heal()
            print(f"{self.name} heals for {self.heal} HP!")

original_mobs_by_floor = {
    1: [
        Slime((1000, 520)),
        Goblin((1270, 350)),
        Slime((1500, 520))
    ],
    2: [
        Slime((1000, 520)),
        Goblin((1270, 350)),
        Goblin((1500, 470)),
    ],
    3: [
        Slime((1000, 520)),
        Goblin((1270, 350)),
        Spider((1600, 540))
    ],
    4: [
        Spider((1100, 540)),
        Goblin((1270, 350)),
        Spider((1600, 540))
    ],
    5: [
        Skeleton((980, 420)),
        Goblin((1270, 350)),
        Goblin((1500, 470))
    ],
    6: [
        Spider((1100, 540)),
        Skeleton((1200, 315)),
        Goblin((1500, 470))
    ],
    7: [
        Skeleton((980, 420)),
        Golem((1300, 290)),
        Spider((1600, 540))
    ],
    8: [
        Skeleton((980, 420)),
        Skeleton((1200, 315)),
        Skeleton((1440, 420))
    ],
    9: [
        Skeleton((980, 420)),
        Golem((1300, 290)),
        Skeleton((1500, 420))
    ],
    10: [
        Skeleton((980, 420)),
        Boss((1250, 290)),
        Golem((1620, 380))
    ],
}

mobs_by_floor = {floor: [copy.copy(mob) for mob in mobs] for floor, mobs in original_mobs_by_floor.items()}