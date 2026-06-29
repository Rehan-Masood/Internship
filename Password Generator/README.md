# PyPassword Generator

A simple Python command-line application that generates a customized, secure password based on user input for the number of letters, symbols, and numbers.

## Features

- **Customizable Length**: Choose exactly how many letters, symbols, and numbers you want in your password.
- **Easy to Use**: Interactive command-line interface prompts you for specifications.
- **Randomized Selection**: Uses Python's `random` module to select characters from predefined lists of letters, numbers, and symbols.

## File Structure

- `Password_Generator`: The main Python script containing the password generation logic.

## Prerequisites

To run this application, you only need Python 3 installed on your system. No external dependencies or libraries are required since it relies entirely on Python's built-in `random` module.

## How to Run

1. Open your terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd "d:/Future/Internship/Projects/Password Generator"
   ```
3. Run the script using Python:
   ```bash
   python Password_Generator
   ```

## Usage Example

```text
Welcome to the PyPassword Generator!
How many letters would you like in your password?
4
How many symbols would you like?
2
How many numbers would you like?
3
Here is your password: gHdX!#729
```

## How It Works

The script contains three predefined lists:
- `letters`: Lowercase and uppercase English letters (`a-z`, `A-Z`).
- `numbers`: Numeric digits (`0-9`).
- `symbols`: Common special characters (`!`, `#`, `$`, `%`, `&`, `(`, `)`, `*`, `+`).

It prompts you for the count of each character type, randomly selects the requested number of elements from each list using `random.choice()`, concatenates them in order (letters first, then symbols, then numbers), and prints the result.

## Suggested Enhancements

Currently, the password is generated in a fixed pattern: all letters first, followed by all symbols, and then all numbers (e.g., `letters` + `symbols` + `numbers`). For stronger security, you can shuffle the password characters:

```python
# To shuffle the password for increased security:
password_list = []

for char in range(1, nr_letters + 1):
    password_list.append(random.choice(letters))

for char in range(1, nr_symbols + 1):
    password_list.append(random.choice(symbols))

for char in range(1, nr_numbers + 1):
    password_list.append(random.choice(numbers))

# Shuffle the list of characters
random.shuffle(password_list)

# Join the shuffled characters into a single string
password = "".join(password_list)
```
