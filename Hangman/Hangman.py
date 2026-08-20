import random

# Notice the 'r' before every triple quote - this tells Python not to treat backslashes as escape sequences
stages = [
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
]

word_list = ["aardvark", "baboon", "camel", "python", "developer"]
chosen_word = random.choice(word_list)
word_length = len(chosen_word)

display = ["_" for _ in range(word_length)]
lives = 6
end_of_game = False

print("Welcome to Hangman!")

while not end_of_game:
    guess = input("Guess a letter: ").strip().lower()

    if not guess or len(guess) != 1:
        print("Please enter a single letter.")
        continue

    if guess in display:
        print(f"You've already guessed '{guess}'.")

    for position in range(word_length):
        letter = chosen_word[position]
        if letter == guess:
            display[position] = letter

    if guess not in chosen_word:
        print(
            f"You guessed '{guess}', that's not in the word. You lose a life."
        )
        lives -= 1
        if lives == 0:
            end_of_game = True
            print(f"You lose. Game Over! The word was: {chosen_word}")

    print(" ".join(display))

    if "_" not in display:
        end_of_game = True
        print("You win! You found the word.")

    print(stages[lives])
