class BudgetAlert:
    """Checks spending against income and warns the user if they're overspending."""

    WARNING_THRESHOLD = 0.8  # warn once expenses reach 80% of income

    @staticmethod
    def check_alert(total_income, total_expense):
        """Prints a warning if expenses have crossed 80% of total income."""
        if total_income == 0:
            return  # nothing to compare against yet

        expense_ratio = total_expense / total_income

        if expense_ratio >= 1:
            print("ALERT: Your expenses have exceeded your total income!")
        elif expense_ratio >= BudgetAlert.WARNING_THRESHOLD:
            print(f"WARNING: You have used {expense_ratio * 100:.1f}% of your income on expenses!")