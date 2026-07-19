# Turtle Crossing Game

A simple Python turtle game where you guide the turtle across the road while avoiding moving cars. Each time you reach the top safely, the level increases and the cars speed up.

## Demo Video
<video src="https://github.com/user-attachments/assets/a3c59786-b7c8-4deb-b9c3-7e3e3319b090" controls width="600"></video>

## Requirements

- Python 3.x
- `turtle` module (included with the standard Python installation)

## How to Run

1. Open a terminal in this folder.
2. Run the main file:

```bash
python main.py
```

If your system uses `python3`, run:

```bash
python3 main.py
```

## Controls

- `Up Arrow`: Move the turtle forward

## Gameplay

- Start at the bottom of the screen.
- Avoid the cars moving across the road.
- Reach the finish line to advance to the next level.
- The game ends if a car hits the turtle.

## Project Files

- `main.py`: Game setup and main loop
- `player.py`: Player turtle logic
- `car_manager.py`: Car spawning and movement
- `scoreboard.py`: Level display and game over text

## Notes

- The game uses only built-in Python libraries.
- Window size is `600 x 600`.
