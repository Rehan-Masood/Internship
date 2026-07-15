import random
from art import logo, vs
from game_data import data


def format_data(account):
    name = account["name"]
    description = account["description"]
    country = account["country"]
    return f"{name}, {description}, from {country}"


def check_answer(guess, a_followers, b_followers):
    if a_followers > b_followers:
        return guess == "a"
    else:
        return guess == "b"


def get_random_account(exclude=None):
    account = random.choice(data)
    while account == exclude:
        account = random.choice(data)
    return account


def game():
    print(logo)
    score = 0
    game_should_continue = True

    account_a = get_random_account()
    account_b = get_random_account(exclude=account_a)

    while game_should_continue:
        print(f"Compare A: {format_data(account_a)}.")
        print(vs)
        print(f"Against B: {format_data(account_b)}.")

        guess = input("Who has more followers? Type 'A' or 'B': ").lower()

        is_correct = check_answer(guess, account_a["follower_count"], account_b["follower_count"])

        if is_correct:
            score += 1
            print(f"You're right! Current score: {score}.\n")
            account_a = account_b
            account_b = get_random_account(exclude=account_a)
        else:
            game_should_continue = False
            print(f"Sorry, that's wrong. Final score: {score}.")


game()

play_again = input("Do you want to play again? (y/n): ")
while play_again.lower() == "y":
    game()
    play_again = input("Do you want to play again? (y/n): ")

print("Thanks for playing!")
