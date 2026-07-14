# Number Guessing Game

A small Python terminal game where the computer chooses a random number between 1 and 100 and the player tries to guess it in as few attempts as possible.

## Overview

The game gives feedback after every guess so the player can narrow down the answer:

- `Too high.` when the guess is above the answer
- `Too low.` when the guess is below the answer
- `You got it!` when the correct number is found

## Features

- Random number generation between 1 and 100
- Two difficulty levels: easy and hard
- Attempt counter that decreases after each incorrect guess
- ASCII art banner shown at startup

## Requirements

- Python 3.x

## Run The Game

Open a terminal in the project folder and run:

```bash
python guessing_game.py
```

If your system uses a different command for Python, you can run the script with that command instead, for example `py guessing_game.py`.

## How To Play

1. Start the game.
2. Choose a difficulty:
   - `easy` gives 10 attempts
   - `hard` gives 5 attempts
3. Enter a guess between 1 and 100.
4. Keep guessing until you find the correct answer or run out of attempts.

## Project Structure

- `guessing_game.py` - main game logic
- `art.py` - ASCII art logo used by the game

## Notes

The game is designed for the terminal and is a good starter project for learning Python basics such as conditionals, loops, and functions.