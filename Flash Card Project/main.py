from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# ----- Load words: continue from where you left off if a "still learning" file exists -----
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    """Picks a new random word and shows the French side, flipping to English after 3 seconds."""
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    """Flips the card over to reveal the English translation."""
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    """Removes the current word from the learning list and saves progress, then shows the next card."""
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ----- Window setup -----
window = Tk()
window.title("Flashy")
window.config(padx=25, pady=15, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# ----- Card canvas -----
canvas = Canvas(width=800, height=450)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 225, image=card_front_img)
card_title = canvas.create_text(400, 130, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 225, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# ----- Buttons -----
cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

# center the window on screen so it doesn't open partly off-screen / behind the taskbar
window.update_idletasks()
window.eval('tk::PlaceWindow . center')

window.mainloop()