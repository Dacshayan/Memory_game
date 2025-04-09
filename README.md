# Memory Game 
## Table of Contents
- [Description](#description)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Rules](#game-rules)
- [Planned Features](#Planned_Features)


## Description
This is a classic Memory Card Game implemented using Python and PyQt5. The game challenges players to find matching pairs of cards by remembering their positions. It supports both single-player and multiplayer modes (up to 4 players).

## Features
- 🎮 Two game modes: Solo and Multiplayer (2-4 players)
- 🔢 Configurable number of card pairs (2-18 pairs)
- 👥 Player name customization
- 📊 Score tracking for each player
- ♻️ Restart game functionality
- 🎨 Clean graphical interface with card images
- 🔄 Turn-based gameplay in multiplayer mode
- 💡 Hint feature 

## Requirements
- Python 3.6+
- PyQt5

### 🔧 Install dependencies  
```sh
pip install PyQt5
```
## 🚀 Usage  
### ▶️ Run the application  
```sh
python Main.py
```
## 📂 File Structure  
```sh
📂 HMI MEMORY PROJECT  
 ├── 📄 Main.py      # Main program file  
 ├── 📂 images     # File with all the images  
 ├── 📄 README.md    # Project documentation  
```

## How to Play
# Basic Game Flow
1. Launch the game by running: python memory_game.py
2. Select your game mode (Solo or Multiplayer)
3. Enter player name(s) when prompted
4. Choose number of card pairs (2-18)
5. Gameplay:
   - Click on any card to flip it
   - Click on a second card to find a match
   - Matching pairs stay flipped
   - Non-matching pairs flip back after 1 second
6. Special Controls:
   - Press 'H' for a hint (reveals a pair for 1 second)
   - Click 'Restart Game' to reset at any time
7. Game ends when all pairs are found

# Solo Mode Rules
- Objective: Find all matching pairs in the fewest moves
- You have unlimited time to complete the game
- Hint system available 

# Multiplayer Mode Rules
- Players take turns in the order they were entered
- Each turn consists of flipping two cards
- Successful match:
  - Player earns 1 point
  - Gets another turn
- Failed match:
  - Cards flip back after 1 second
  - Turn passes to next player
- Winner is player with most points when all pairs are found
- Tiebreaker: First player to reach the high score wins

# General Rules
- Each card has exactly one match
- Cards must be matched by identical values
- Hints reveal matches but don't count toward score

# Planned Features
- [ ] Difficulty Levels:
      Easy (8 pairs), Medium (12 pairs), Hard (18 pairs)
      
- [ ] Timed Mode:
      Add countdown timer with 2min/5min/10min options

- [ ] Enhanced Scoring:
      - Points based on time remaining
      - Bonus for consecutive matches
      - Penalty for using hints

- [ ] Audio Effects:
      - Add sound for matches, flips, and victory
      - Background music toggle

- [ ] Visual Enhancements:
      - Card flip animations
      - Victory fireworks effect
      - Player avatars

- [ ] Advanced Features:
      - Save/Load game state
      - Online multiplayer
      - Daily challenges
      - Card themes selector

## 👥 Contributors  
**The Team** : Dacshayan JEYANESHAN, Kavinan KANDAVEL
