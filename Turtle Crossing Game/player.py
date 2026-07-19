from turtle import Turtle

STARTING_POSITION = (0, -280)
MOVE_DISTANCE = 10
FINISH_LINE_Y = 280


class Player(Turtle):
    """The turtle the player controls, moving from bottom to top."""

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.color("black")
        self.penup()
        self.setheading(90)  # face upward
        self.go_to_start()

    def go_to_start(self):
        self.goto(STARTING_POSITION)

    def go_up(self):
        new_y = self.ycor() + MOVE_DISTANCE
        self.goto(self.xcor(), new_y)

    def has_reached_finish_line(self):
        """Returns True once the player has crossed the top of the screen."""
        return self.ycor() > FINISH_LINE_Y
