# Turtle Race

A small interactive Python turtle graphics project where colored turtles race across the screen and you place a bet on which one will win.

## Features
- Simple GUI input prompt to place a bet on a turtle color.
- Uses Python's built-in `turtle` module for graphics and animation.
- Cross-platform but includes a Windows DPI fix for clearer rendering on high-DPI displays.

## Prerequisites
- Python 3.8 or newer (the `turtle` module is part of the standard library).

## Available turtle colors
red, orange, yellow, green, blue, purple

## Run
1. Open a terminal in the project folder.
2. Run:

```
python main.py
```

3. A small dialog will prompt you to enter a color to bet on. Type one of the available colors and press OK.
4. The race will start; the program prints the result to the console and displays it on the canvas. Click the window to exit.

## Notes
- If the text-input dialog doesn't appear on top on some platforms, check your window manager or run the script from a terminal.
- The program prints the result to the console and also renders the outcome on the turtle screen.

## Files
- `main.py`: the race simulation and UI.

If you want, I can add a requirements file, packaging, or a short GIF showing the game in action.
