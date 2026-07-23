# Pomodoro App

A simple desktop Pomodoro timer built with Python and Tkinter.

## Demo Video
<video src="https://github.com/user-attachments/assets/9cef9586-d73c-4b96-b2ea-68bd9eb187f9" controls width="600"></video>

## Features

- 25-minute focus sessions
- 5-minute short breaks
- 15-minute long break after 4 work sessions
- Visual timer display with progress check marks
- Start and reset controls

## Requirements

- Python 3.x
- Tkinter, which is included with most standard Python installations

## How to Run

1. Open a terminal in the project folder.
2. Run the app:

```bash
python main.py
```

## Project Files

- `main.py` - main application logic and UI
- `tomato.png` - image used in the timer display

## How It Works

The timer alternates between work sessions and breaks:

- Work session: 25 minutes
- Short break: 5 minutes
- Long break: 15 minutes after every 4 work sessions

The app automatically updates the countdown and adds a check mark after each completed work session.

## Notes

- Keep `main.py` and `tomato.png` in the same folder so the image loads correctly.
- If Tkinter is missing on your system, install the Python distribution that includes it or enable the Tkinter package for your platform.
