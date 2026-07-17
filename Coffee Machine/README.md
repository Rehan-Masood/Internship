# Coffee Machine (Python)

A simple command-line coffee machine simulator written in Python.

## Coffee Machine
   ![Coffee Machine.](./Coffee%20Machine.jpg)

## Project Overview

This project simulates a coffee machine that can:
- Serve three drinks: espresso, latte, and cappuccino
- Track available resources (water, milk, coffee)
- Accept coin input and process payment
- Return change when extra money is inserted
- Print a machine report
- Turn off the machine

## File Structure

- `Coffee.py` - Main Python script containing the full simulation logic

## Requirements

- Python 3.x

No external libraries are required.

## How to Run

1. Open a terminal in the project folder.
2. Run:

   ```bash
   python Coffee.py
   ```

## How to Use

When prompted:
- Enter `espresso`, `latte`, or `cappuccino` to buy a drink
- Enter `report` to display current resources and total money collected
- Enter `off` to stop the machine

For drink orders:
1. The machine checks if enough resources are available.
2. If available, it asks for coins:
   - quarters
   - dimes
   - nickles
   - pennies
3. It processes payment, returns change if needed, and serves the drink.

## Notes

- The script uses in-memory values, so resources and profit reset each time you restart the program.
- Coin label is written as `nickles` in the current script to match the existing code prompt.

## Example Session

- Input: `report`
- Input: `latte`
- Insert coins when asked
- Input: `off`
