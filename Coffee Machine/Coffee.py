MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    },
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

profit = 0
machine_on = True

while machine_on:
    choice = input("What would you like? (espresso/latte/cappuccino): ").lower()

    if choice == "off":
        machine_on = False

    elif choice == "report":
        print(f"Water: {resources['water']}ml")
        print(f"Milk: {resources['milk']}ml")
        print(f"Coffee: {resources['coffee']}g")
        print(f"Money: ${profit}")

    elif choice in MENU:
        drink = MENU[choice]
        ingredients = drink["ingredients"]

        enough_resources = True
        for item in ingredients:
            if ingredients[item] > resources[item]:
                print(f"Sorry there is not enough {item}.")
                enough_resources = False

        if enough_resources:
            print("Please insert coins.")
            quarters = int(input("How many quarters?: "))
            dimes = int(input("How many dimes?: "))
            nickles = int(input("How many nickles?: "))
            pennies = int(input("How many pennies?: "))

            total_inserted = (quarters * 0.25) + (dimes * 0.1) + (nickles * 0.05) + (pennies * 0.01)

            if total_inserted < drink["cost"]:
                print("Sorry that's not enough money. Money refunded.")
            else:
                change = round(total_inserted - drink["cost"], 2)
                if change > 0:
                    print(f"Here is ${change} in change.")

                for item in ingredients:
                    resources[item] -= ingredients[item]

                profit += drink["cost"]
                print(f"Here is your {choice}. Enjoy!")

    else:
        print("Sorry, that's not a valid option.")