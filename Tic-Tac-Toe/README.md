# Python Tic-Tac-Toe

A simple, terminal-based Tic-Tac-Toe game written in Python.

## Demo Video
<video src="https://github.com/user-attachments/assets/305cc328-cf86-4309-9425-d0481ca873ac" controls width="600"></video>

## Description

This project provides a local two-player and single-player Tic-Tac-Toe game. The single-player mode offers three difficulty levels: Easy (random moves), Medium (basic tactics), and Hard (unbeatable Minimax AI).

## Features

- Play against the computer or a second human player.
- Three AI difficulty levels (Easy / Medium / Hard).
- Clean terminal UI and simple controls.

## Requirements

- Python 3.8 or newer

## Files

- [main.py](main.py) — The main game script.

## Usage

Run the game from the project root:

```bash
python main.py
```

Follow on-screen prompts to choose game mode and, if applicable, AI difficulty.

Controls:
- Enter a number from `1` to `9` to place your mark on the board positions as shown.
- Enter `q`, `quit`, or `exit` to leave the game at any prompt.

Board positions mapping:

```
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9
```

## AI Difficulty

- Easy — computer plays random valid moves.
- Medium — computer looks for immediate wins or blocks, prefers center.
- Hard — computer uses the Minimax algorithm for optimal play.

## Contributing

Contributions are welcome. Open an issue or submit a pull request with improvements or bug fixes.

## License

This project is provided as-is. Add a LICENSE file if you want to specify terms.
