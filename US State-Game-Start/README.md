# U.S. States Game

A simple Turtle-based geography game built with Python. The goal is to name all 50 U.S. states by typing them into the prompt while they are placed on the map.

## Features

- Interactive map quiz using the Python `turtle` module
- Tracks correct guesses on the map
- Saves missed states to `states_to_learn.csv` when you exit

## Requirements

- Python 3.x
- `pandas`

## Project Files

- `main.py` - game entry point
- `50_states.csv` - state names with map coordinates
- `blank_states_img.gif` - background map image used by the game
- `states_to_learn.csv` - created after exiting the game with unfinished states

## How to Run

1. Install the required package:

   ```bash
   pip install pandas
   ```

2. Run the game:

   ```bash
   python main.py
   ```

## How To Play

- Type a U.S. state name into the prompt.
- Correct answers appear on the map at the right location.
- Type `Exit` to quit early and save the remaining states to `states_to_learn.csv`.

## Notes

- Make sure `blank_states_img.gif` is in the same folder as `main.py`.
- The game uses the coordinate data in `50_states.csv` to place each state label on the map.