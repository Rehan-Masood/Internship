# Password Manager 

A simple desktop password manager built with Python and Tkinter.

## Demo Video
<video src="https://github.com/user-attachments/assets/808de202-5059-469e-873d-e7509b6a2a77" controls width="600"></video>

## Password Mananger
   ![Password Mananger .](./Password%20Manager.jpg)

## Data Storage 
   ![Data Storage .](./Data%20Storage.jpg)


This app helps you:
- Generate strong random passwords
- Copy generated passwords to your clipboard automatically
- Save website login details to a local file

## Features

- GUI built with Tkinter
- Password generation using letters, numbers, and symbols
- One-click copy using `pyperclip`
- Save credentials in `data.txt` with confirmation dialog

## Project Structure

- `main.py`: Main application code
- `data.txt`: Stored credentials (plain text)
- `logo.png`: App logo shown in the UI
- `pyproject.toml`: Poetry project/dependency config

## Requirements

- Python 3.8+
- `pyperclip`

## Setup

### Option 1: Using Poetry

```bash
poetry install
poetry run python main.py
```

### Option 2: Using pip + venv

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pyperclip
python main.py
```

## How to Use

1. Enter a website name.
2. Enter email/username (or keep your default value).
3. Click **Generate Password** to create a secure password.
4. Click **Add** and confirm to save the credentials.

Saved entries are appended to `data.txt` in this format:

```text
website | email | password
```

## Important Note

This project stores passwords in plain text inside `data.txt`.
It is suitable for learning and practice, but not for production or real sensitive data.

## Screenshots

- `Password Manager.jpg`
- `Data Storage.jpg`
