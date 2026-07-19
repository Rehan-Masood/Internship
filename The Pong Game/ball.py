from turtle import Turtle

MOVE_SPEED = 0.1


class Ball(Turtle):
    """The ball that bounces around and speeds up over time."""

    def __init__(self):
        super().__init__()
        self.color("white")
        self.shape("circle")
        self.penup()
        self.x_move = 10
        self.y_move = 10
        self.move_speed = MOVE_SPEED

    def move(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)

    def bounce_y(self):
        """Reverses vertical direction (used when hitting top/bottom wall)."""
        self.y_move *= -1

    def bounce_x(self):
        """Reverses horizontal direction and speeds up slightly (used when hitting a paddle)."""
        self.x_move *= -1
        self.move_speed *= 0.9  # game gets a little faster after every paddle hit

    def reset_position(self):
        """Sends the ball back to the center and reverses its horizontal direction,
        so it starts heading towards whoever just conceded the point."""
        self.goto(0, 0)
        self.move_speed = MOVE_SPEED
        self.bounce_x()
