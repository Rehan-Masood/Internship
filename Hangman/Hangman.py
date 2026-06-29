import random

stages = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']

word_list = ["ardvark", "baboon", "camel", "python", "developer"]
chosen_word = random.choice(word_list)
word_length = len(chosen_word)

display = ["_" for _ in range(word_length)]
lives = 6
end_of_game = False

print("Welcome to Hangman!")
while not end_of_game:
    guess = input("Guess a letter: ").lower()
    if guess in display:
        print("You've already guessed", guess)
    for position in range(word_length):
        letter = chosen_word[position]
        if letter == guess:
            display[position] = letter
    if guess not in chosen_word:
        print("You guessed", guess, "that's not in the word. You lose a life.")
        lives -= 1
        if lives == 0:
            end_of_game = True
            print("You lose. Game Over.")
    print(" ".join(display))
    if "_" not in display:
        end_of_game = True
        print("You win! You found the treasure/word.")
    print(stages[lives])