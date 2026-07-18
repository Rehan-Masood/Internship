# Snake Game

A simple Snake game built with Python's built-in `turtle` module. The player controls the snake with the arrow keys, eats food to grow, and tries to avoid the walls and its own body.

## Features

- Classic Snake gameplay with keyboard controls
- Random food spawning inside the play area
- Score tracking during play
- Game over on wall collision or self-collision

## Requirements

- Python 3.x
- No third-party packages are required

## How to Run

1. Open a terminal in this folder.
2. Run the game:

```bash
python main.py
```

If your system uses `python3` instead of `python`, run:

```bash
python3 main.py
```

## Controls

- Up Arrow: move up
- Down Arrow: move down
- Left Arrow: move left
- Right Arrow: move right

## Project Structure

- `main.py` - starts the game loop and handles collisions
- `snake.py` - snake movement and growth logic
- `food.py` - food placement and respawn logic
- `scoreboard.py` - score display and game-over text

## Notes

- The game window uses the full available screen size.
- On Windows, the game tries to enable DPI awareness for better scaling.