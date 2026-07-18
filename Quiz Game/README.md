# Quiz Game

A small Python console quiz that asks 5 random true/false questions from a built-in question bank and shows your final score at the end.

## Demo Video
<video src="https://github.com/user-attachments/assets/aa102add-920d-4149-b5e3-2e5cf86e959b" controls width="600"></video>

## Quiz Game 
   ![Quiz Game .](./Quiz%20Game.jpg)

## Features

- Randomly selects 5 questions each time you run the program
- Accepts `True`, `False`, `T`, or `F` as answers
- Keeps track of your score as you play
- Shows the correct answer after each question

## Requirements

- Python 3.x

## How to Run

From the project folder, run:

```bash
python main.py
```

## Project Structure

- `main.py` - Starts the quiz and controls the game loop
- `quiz_brain.py` - Handles question flow, input validation, and scoring
- `question_model.py` - Defines the `Question` class
- `data.py` - Stores the quiz questions

## Example

```text
Q.1: A slug's blood is green. (True/False)?: true
You got it right!
The correct answer was: True.
Your current score is: 1/1.
```

## Notes

- Questions are stored in `data.py`, so you can add or edit questions there.
- The quiz uses `random.sample`, so the 5 questions are different on each run.
