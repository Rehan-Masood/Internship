# Morse Code Converter

A small Python CLI tool that converts plain text into Morse code.

## Demo Video
<video src="" controls width="600"></video>

## Morse Code Converter
   ![Morse Code Converter.](./1jpg)

## Features
- Converts letters, digits, and common punctuation to Morse code.
- Prints unknown characters as `[?]` so outputs remain readable.
- Simple interactive command-line interface.

## Requirements
- Python 3.7+

## Installation
1. Clone or download this repository.
2. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies (none required for this simple script).

## Usage
Run the converter from the project root:

```powershell
python main.py
```

The program runs interactively. Type any message and press Enter to see the Morse code translation. Type `exit`, `q`, or `quit` to end the program.

Example:

```
Enter text: Hello World

RESULT (Morse Code):
.... . .-.. .-.. --- / .-- --- .-. .-.. -..
```

## How it works
The core conversion uses a dictionary mapping characters to Morse sequences (see `main.py`). Words are separated with ` / ` and letters with spaces.

## Contribution
Feel free to open issues or send pull requests to add features such as:
- File input/output
- Support for customizable separators or timing (for audio/LED signalling)
- Command-line flags for non-interactive use

## License
This project is provided under the MIT license — modify as you prefer.
