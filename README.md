# Dungeon Descend

A turn-based card game built with Pygame where you descend through a challenging dungeon with strategic deck building.

![Game Preview](Sprites/game_title.png)

## Game Description

Dungeon Descend is a strategic card-based roguelike where you must fight your way through 10 increasingly difficult dungeon floors to defeat the final boss.

### Key Features:
- **Deck Building**: Start with 10 cards (5 attack, 5 shield) and build your deck up to 15 cards
- **Turn-Based Combat**: Use 3 energy per turn to play cards from your hand
- **Progressive Difficulty**: Navigate through 10 dungeon floors with increasingly challenging enemies
- **Strategic Choices**: Choose rewards after each successful floor to improve your deck
- **Boss Battle**: Confront the dungeon boss on the final floor for the ultimate challenge

### Game Mechanics:
- Your character starts with 50 health
- Draw 5 random cards into your hand each turn
- Use energy to play attack and defense cards
- Cards go to discard pile after use, which reshuffles into your deck when empty
- After defeating enemies, choose new cards from treasure chests to improve your deck

## Setup Instructions

### Prerequisites
- Python 3.x
- Pygame
- MoviePy (for cutscenes)

### Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/dungeon-descend.git
cd dungeon-descend
```

2. Install required dependencies:
```
pip install pygame moviepy
```

3. Run the game:
```
python start.py
```

## Controls
- Use your mouse to select and play cards
- Click on cards and drag them to the play area
- Use the "End Turn" button when you've finished your actions

## Development

This game was developed using:
- Python 3.x
- Pygame for game mechanics and rendering
- Custom pixel art assets
- Custom sound effects and music
 