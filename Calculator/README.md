# Python Command-Line Calculator

A clean, interactive, command-line calculator written in Python. It allows users to perform basic arithmetic operations and chain multiple calculations together continuously.

## Features

- **Basic Operations**: Supports addition, subtraction, multiplication, and division.
- **Continuous Mode**: Chain new operations directly onto the result of your previous calculation.
- **Interactive Console UI**: Features a custom ASCII art logo and intuitive prompts.
- **Session Restart**: Easily reset the calculator state to start a completely new calculation session.

## File Structure

- [Calculator.py](file:///d:/Future/Internship/Projects/Calculator/Calculator.py): The main application containing the calculator logic, arithmetic functions, and interaction loop.
- [art.py](file:///d:/Future/Internship/Projects/Calculator/art.py): Contains the ASCII art used for the application's startup header.

## How to Run

1. Make sure you have Python 3 installed on your system.
2. Clone or navigate to the project directory:
   ```bash
   cd d:/Future/Internship/Projects/Calculator
   ```
3. Run the application:
   ```bash
   python Calculator.py
   ```

## Usage Example

```text
 _____________________
|  _________________  |
| | Pythonista   0. | |
| |_________________| |
|  ___ ___ ___   ___  |
| | 7 | 8 | 9 | | + | |
| |___|___|___| |___| |
| | 4 | 5 | 6 | | - | |
| |___|___|___| |___| |
| | 1 | 2 | 3 | | x | |
| |___|___|___| |___| |
| | . | 0 | = | | / | |
| |___|___|___| |___| |
|_____________________|

What's the first number?: 10
+
-
*
/
Pick an operation: +
What's the next number?: 5
10.0 + 5.0 = 15.0
Type 'y' to continue calculating with 15.0, or type 'n' to start a new calculation: y
Pick an operation: *
What's the next number?: 2
15.0 * 2.0 = 30.0
Type 'y' to continue calculating with 30.0, or type 'n' to start a new calculation: n
```
