# 🏴‍☠️ Treasure Island Adventure Game

Welcome to **Treasure Island**, a classic text-based interactive adventure game written in Python! 

Your mission, should you choose to accept it, is to navigate a series of dangerous choices, avoid deadly traps, and find the hidden treasure.

---

## 🎮 How to Play

The game will prompt you to make decisions at key moments. Type your choices in the terminal when prompted and press **Enter**.

### The Flow of Choices
1. **The Crossroads**: Choose between going `left` or `right`.
2. **The Lake**: Choose to `wait` for a boat or `swim` across.
3. **The Island House**: Choose between three doors: `red`, `yellow`, or `blue`.

Choose wisely—one wrong move, and the game is over!

---

## 🚀 Getting Started

### Prerequisites
You need **Python 3** installed on your system to run the game. You can check your version using:
```bash
python --version
```

### Running the Game
Navigate to the project directory and run the script:
```bash
python Treasure_Island.py
```

---

## 📝 Game Logic & Rules (Spoiler Alert! ⚠️)

If you are struggling to find the treasure, here is a hint of the game's branching logic:

```mermaid
graph TD
    Start([Welcome to Treasure Island]) --> Choice1{Crossroad Choice}
    Choice1 -->|right| Hole[Fell into a hole. Game Over!]
    Choice1 -->|left| Choice2{Lake Choice}
    
    Choice2 -->|swim| Trout[Attacked by angry trout. Game Over!]
    Choice2 -->|wait| Choice3{Door Choice}
    
    Choice3 -->|red| Fire[Room full of fire. Game Over!]
    Choice3 -->|blue| Beasts[Room of beasts. Game Over!]
    Choice3 -->|yellow| Win[You found the treasure! You Win! 🎉]
    Choice3 -->|other| NonExistent[Door doesn't exist. Game Over!]
```

---

## 🛠️ Code Overview

The game is built entirely in Python using simple conditional structures (`if-elif-else`) and standard input/output. It is a great starting project for beginners learning control flow in Python.

- **File**: `Treasure_Island.py`
- **Language**: Python 3.x
- **Key Concepts**: Input handling, lowercasing strings for robust comparison, nested conditional statements.
