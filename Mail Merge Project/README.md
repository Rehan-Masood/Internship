# Mail Merge Project (Python)

A simple Python mail merge script that reads a list of names and a letter template, then generates one personalized text file per person.

## Features

- Reads names from `Input/Names/invited_names.txt`
- Reads template from `Input/Letters/starting_letter.txt`
- Replaces `[name]` placeholder with each person's name
- Creates personalized files in `Output/ReadyToSend/`

## Project Structure

```text
Mail Merge Project/
├── main.py
├── Input/
│   ├── Letters/
│   │   └── starting_letter.txt
│   └── Names/
│       └── invited_names.txt
└── Output/
    └── ReadyToSend/
```

## Requirements

- Python 3.x
- No external libraries required (uses built-in Python only)

## How to Run

1. Open a terminal in the project folder.
2. Run:

```bash
python main.py
```

After running, the script creates one file per name in `Output/ReadyToSend/`.

## Input Format

### `Input/Letters/starting_letter.txt`

Use `[name]` where the recipient name should appear.

Example:

```text
Dear [name],

You are invited to my birthday this Saturday.

Hope you can make it!
```

### `Input/Names/invited_names.txt`

Write one name per line.

Example:

```text
Abdullah
Faizan
Faraz
```

## Output Example

If `Abdullah` is in the names list, this file is generated:

- `Output/ReadyToSend/letter_for_Abdullah.txt`

## Notes

- Keep the placeholder exactly as `[name]` in the template.
- Make sure the `Output/ReadyToSend/` folder exists before running.
- The script trims extra spaces/newlines around names automatically.
