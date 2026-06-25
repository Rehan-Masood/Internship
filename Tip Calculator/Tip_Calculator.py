print("Welcome to the Tip Calculator!")
Total_bill = float(input("What was the total bill? $"))
Tip = int(input("How much tip would you like to give? 10, 20, or 15? "))
people = int(input("How many people to split the bill? "))
Final_amount = (Total_bill +(Total_bill * Tip / 100)) / people
print("Each person should pay : $", round(Final_amount, 2))
