import random
from flask import Flask

app = Flask(__name__)

random_number = random.randint(0, 9)
print(f"DEBUG: Secret target number is {random_number}")


@app.route("/")
def home():
    """Home page asking the user to guess a number."""
    return (
        "<h1>Guess a number between 0 and 9</h1>"
        '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" width="350">'
    )


@app.route("/<int:guess>")
def check_guess(guess):
    """Route to catch dynamic URL input and compare against the random number."""
    if guess < random_number:
        return (
            '<h1 style="color: red;">Too low, try again!</h1>'
            '<img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif" width="400">'
        )
    elif guess > random_number:
        return (
            '<h1 style="color: purple;">Too high, try again!</h1>'
            '<img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif" width="400">'
        )
    else:
        return (
            '<h1 style="color: green;">You found me!</h1>'
            '<img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif" width="400">'
        )


if __name__ == "__main__":
    app.run(debug=True)