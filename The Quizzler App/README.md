# The Quizzler App

A small Python quiz application with a simple GUI.

## Overview

The Quizzler App is a lightweight quiz program that presents multiple-choice or true/false questions to the user, tracks score, and provides a simple GUI. It is implemented in Python using a small MVC-like separation:

- `data.py` — question data source.
- `question_model.py` — `Question` model class.
- `quiz_brain.py` — quiz logic and scoring (`QuizBrain`).
- `ui.py` — graphical user interface (Tkinter).
- `main.py` — application entry point.
- `images/` — folder for any UI images used by the app.

## Requirements

- Python 3.10+ (the project was tested with Python 3.13).
- The GUI uses the standard library (`tkinter`) so there are no required external packages by default.

If your project adds third-party dependencies, list them in `requirements.txt` and install with:

```
pip install -r requirements.txt
```

## Run

From the project root run:

```
python main.py
```

This will launch the quiz GUI.

## Project structure

- `main.py` — starts the app and wires together the UI and quiz logic.
- `ui.py` — builds the Tkinter interface and handles user interaction.
- `quiz_brain.py` — contains the quiz engine (question selection, score updates).
- `question_model.py` — defines the `Question` data structure used by the engine.
- `data.py` — contains or loads the question set used by the quiz.
- `images/` — assets used by the UI.

## Contributing

Contributions are welcome. Suggested workflow:

1. Create a branch for your feature or fix.
2. Run the app locally and verify behavior.
3. Open a pull request with a short description of changes.

## License

This project has no license specified. If you want to add one, create a `LICENSE` file (for example, `MIT`).

---

If you'd like, I can add a `requirements.txt`, package it with a basic virtualenv setup, or expand the README with screenshots and examples from your current UI. Which would you prefer?
