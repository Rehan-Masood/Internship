# Coffee Machine OOP Project

A Python-based vending machine simulator that demonstrates Object-Oriented Programming (OOP) principles. This project implements a fully functional coffee machine with menu management, resource tracking, and payment processing.

## Demo Video
<video src="https://github.com/user-attachments/assets/64530241-700a-4179-8fb1-b8e8d6daa8c2" controls width="600"></video>

## Coffee Machine
   ![Coffee Machine.](./Coffee%20Machine.jpg)

## Features

- **Multiple Drink Options**: Choose from Latte, Espresso, and Cappuccino
- **Resource Management**: Track water, milk, and coffee levels
- **Payment Processing**: Accept coin payments (quarters, dimes, nickels, pennies)
- **Change Calculation**: Automatically calculates and returns change
- **Machine Reports**: Check resource levels and profit at any time
- **OOP Architecture**: Demonstrates inheritance, encapsulation, and modular design

## Project Structure

```
Coffee Machine (OOP)/
├── main.py              # Main program entry point and event loop
├── coffee_maker.py      # CoffeeMaker class - handles drink preparation
├── menu.py              # Menu and MenuItem classes - manages drink options
├── money_machine.py     # MoneyMachine class - handles payments and profit
└── README.md            # This file
```

## Classes Overview

### CoffeeMaker
Manages the coffee machine's resources and drink preparation.
- **Methods**:
  - `report()`: Display current resource levels
  - `is_resource_sufficient(drink)`: Check if ingredients are available
  - `make_coffee(order)`: Prepare drink and deduct ingredients

### MenuItem
Represents a single drink on the menu.
- **Attributes**: name, cost, ingredients dictionary

### Menu
Manages the drink menu.
- **Methods**:
  - `get_items()`: Display all available drinks
  - `find_drink(order_name)`: Look up a drink by name

### MoneyMachine
Handles payment processing and profit tracking.
- **Methods**:
  - `report()`: Display total profit
  - `process_coins()`: Accept coin payments
  - `make_payment(cost)`: Process and validate payment

## Menu Items & Pricing

| Drink | Price | Ingredients |
|-------|-------|-------------|
| Espresso | $1.50 | 50ml water, 18g coffee |
| Latte | $2.50 | 200ml water, 150ml milk, 24g coffee |
| Cappuccino | $3.00 | 250ml water, 100ml milk, 24g coffee |

## How to Run

1. Navigate to the project directory:
   ```bash
   cd "Coffee Machine (OOP)"
   ```

2. Run the program:
   ```bash
   python main.py
   ```

## Usage Example

```
What would you like? (espresso/latte/cappuccino/): latte
Please insert coins.
How many quarters?: 10
Here is your latte. Enjoy!
```

## Commands

- **Order a drink**: Enter the drink name (espresso, latte, cappuccino)
- **`report`**: Display resource levels and profit
- **`off`**: Turn off the machine and exit

## Initial Resources

- Water: 300ml
- Milk: 200ml
- Coffee: 100g

## Requirements

- Python 3.x

## OOP Principles Demonstrated

- **Encapsulation**: Each class encapsulates related data and methods
- **Modularity**: Separate classes for different responsibilities
- **Abstraction**: Complex operations hidden behind simple interfaces
- **Data Structures**: Dictionaries for managing ingredients and resources

## Future Enhancements

- Add more drink options
- Implement resource refill functionality
- Add transaction history
- Implement error handling for invalid inputs
- Create a GUI interface

## Author

Created as an OOP learning project for internship program.

## License

This project is open source and available for educational purposes.
