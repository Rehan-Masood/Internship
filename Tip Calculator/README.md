# Tip Calculator

A simple and interactive command-line interface (CLI) Python utility designed to calculate the exact amount each person needs to pay when splitting a bill, incorporating a custom tip percentage.

## Screenshot
# Tip Calculator
![Tip Calculator.](./Tip%20Calculator.jpg)

## Features

- **Interactive Prompts**: Asks for the total bill, desired tip percentage, and the number of people sharing the bill.
- **Tip Calculations**: Dynamically computes the tip and adds it to the total bill.
- **Equal Bill Splitting**: Evenly distributes the final amount among all individuals.
- **Precise Output**: Automatically rounds the share per person to two decimal places.

## Prerequisites

To run this application, you only need to have **Python 3.x** installed on your system.

## How to Run

1. Clone or download this repository.
2. Open your terminal, PowerShell, or command prompt.
3. Navigate to the project directory:
   ```bash
   cd "Tip Calculator"
   ```
4. Run the script:
   ```bash
   python Tip_Calculator.py
   ```

## Example Usage

Here is a quick example of how the interactive tool works:

```text
Welcome to the Tip Calculator!
What was the total bill? $150.00
How much tip would you like to give? 10, 20, or 15? 15
How many people to split the bill? 5
Each person should pay : $ 34.5
```

## Code Overview

The script is defined in [Tip_Calculator.py](file:///d:/Future/Internship/Projects/Tip%20Calculator/Tip_Calculator.py) and executes the following logic:

```python
print("Welcome to the Tip Calculator!")
Total_bill = float(input("What was the total bill? $"))
Tip = int(input("How much tip would you like to give? 10, 20, or 15? "))
people = int(input("How many people to split the bill? "))
Final_amount = (Total_bill +(Total_bill * Tip / 100)) / people
print("Each person should pay : $", round(Final_amount, 2))
```
