import random
import sys
from turtle import Turtle, Screen

# ----- Make this app DPI-aware on Windows -----
# Without this, Windows renders the turtle window at a smaller "virtual"
# resolution and just visually stretches it to look full-screen on your
# monitor. Screen recorders (like Xbox Game Bar) capture the real,
# un-stretched buffer though, so the recording shows the window small in
# a corner. Setting DPI awareness makes the app render at true resolution.
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except Exception:
        pass  # safe to ignore if this fails (e.g. older Windows versions)

is_race_on = False

# ----- Set up the screen -----
screen = Screen()
screen.setup(width=1.0, height=1.0)

# get the actual window size (in pixels) now that the window is maximized
window_width = screen.window_width()
window_height = screen.window_height()

# leave some margin on each side so turtles don't spawn/finish off-screen
start_x = -window_width / 2 + 100
finish_x = window_width / 2 - 100

# ----- Ask the player to place their bet -----
user_bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color: ")

colors = ["red", "orange", "yellow", "green", "blue", "purple"]

# spread the 6 turtles evenly across the height of the window
lane_height = (window_height - 200) / len(colors)
y_positions = [-((window_height - 200) / 2) + (i * lane_height) for i in range(len(colors))]

all_turtles = []

# ----- Create 6 turtles, one for each color, lined up on the left -----
for turtle_index in range(0, 6):
    tim = Turtle(shape="turtle")
    tim.shapesize(stretch_wid=2, stretch_len=2)
    tim.penup()
    tim.color(colors[turtle_index])
    tim.goto(x=start_x, y=y_positions[turtle_index])
    all_turtles.append(tim)

# ----- A dedicated turtle just for writing the result on screen -----
announcer = Turtle()
announcer.hideturtle()
announcer.penup()
announcer.goto(0, window_height / 2 - 100)

# ----- Only start the race if the player entered a bet -----
if user_bet:
    is_race_on = True

# ----- Race loop: keep moving turtles forward until one crosses the finish line -----
while is_race_on:

    for turtle in all_turtles:
        # move each turtle forward by a random distance
        rand_distance = random.randint(0, 15)
        turtle.forward(rand_distance)

        # check if this turtle has crossed the finish line
        if turtle.xcor() > finish_x:
            is_race_on = False

            winning_color = turtle.pencolor()

            if winning_color == user_bet:
                result_text = f"You've won! The {winning_color} turtle is the winner!"
            else:
                result_text = f"You've lost! The {winning_color} turtle is the winner!"

            print(result_text)
            announcer.write(result_text, align="center", font=("Arial", 16, "normal"))

            # stop checking the rest of the turtles this round so we don't
            # write the result message more than once
            break

screen.exitonclick()