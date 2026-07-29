# Flash Card Project

A simple Python flashcard app built with Tkinter to help users learn French vocabulary. The app displays a French word, flips to its English translation after a few seconds, and lets the user mark words as known or unknown.

## Demo Video
<video src="https://github.com/user-attachments/assets/ecf313de-913b-487a-b3c5-831c8eb4a844" controls width="600"></video>

## Features
- Displays French vocabulary cards
- Automatically flips to the English meaning after 3 seconds
- Lets the user mark a word as known or unknown
- Saves progress in a CSV file so learning continues from where you left off

## Project Structure
- `main.py` – Main application code
- `data/french_words.csv` – Original vocabulary list
- `data/words_to_learn.csv` – Updated list of words still being learned
- `images/` – Card and button images used by the GUI

## Requirements
- Python 3.x
- pandas
- Tkinter (usually included with Python)

## Installation
Install the required package:

```bash
pip install pandas
```

## How to Run
Run the application from the project folder:

```bash
python main.py
```

## How It Works
1. The app loads words from the CSV file.
2. A random French word is shown on the card.
3. After 3 seconds, the card flips to reveal the English translation.
4. If the word is known, it is removed from the learning list and saved.
5. If the word is unknown, the next card appears.

## Notes
- The app uses the file `data/words_to_learn.csv` to remember your progress.
- If that file does not exist, it starts from the original vocabulary list.
