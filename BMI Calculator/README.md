# Rehan's BMI Calculator

A simple desktop BMI Calculator built with Python and Tkinter. Enter your weight in kilograms and height in centimeters to calculate your Body Mass Index and see the result category.

## BMI Calculator
![BMI Calculator.]()

## Features

- Clean Tkinter desktop interface
- Calculates BMI from weight and height
- Shows BMI category:
  - Underweight
  - Normal weight
  - Overweight
  - Obese
- Displays validation messages for invalid or empty input

## Requirements

- Python 3.x
- Tkinter (included with most standard Python installations)

## How to Run

1. Open a terminal in the project folder.
2. Run the script:

```bash
python BMI.py
```

## How It Works

- Weight is entered in kilograms.
- Height is entered in centimeters.
- BMI is calculated with the formula:

```text
BMI = weight / (height_in_meters ^ 2)
```

## BMI Categories

- Below 18.5: Underweight
- 18.5 to 24.9: Normal weight
- 25.0 to 29.9: Overweight
- 30.0 and above: Obese

## Notes

- The app checks that values are greater than zero.
- If the input is not a number, the app shows an error message instead of crashing.
