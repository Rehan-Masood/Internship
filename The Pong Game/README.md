# The Pong Game

A simple two-player Pong game built with Python's built-in `turtle` module.

## Demo Video
<video src="https://github.com/user-attachments/assets/76c86a38-0538-40d7-93e3-6e2bbd67f490" controls width="600"></video>

## Features

- Classic Pong-style gameplay
- Two paddles controlled by separate players
- Ball movement with bouncing physics
- Score tracking for both players
- Simple, lightweight implementation with no external dependencies

## How to Run

1. Make sure Python is installed on your system.
2. Open a terminal in the project folder.
3. Run:

```bash
python main.py
```

## Controls

- Left paddle: `W` to move up, `S` to move down
- Right paddle: `Up Arrow` to move up, `Down Arrow` to move down

## Project Structure

- `main.py` - Runs the game loop and sets up the screen
- `paddle.py` - Defines the paddle behavior and movement
- `ball.py` - Handles ball movement, bouncing, and reset logic
- `scoreboard.py` - Tracks and displays player scores

## Requirements

- Python 3.x
- No additional packages required

## Notes

The game uses the built-in turtle graphics library, so it should work on most systems with Python installed.
