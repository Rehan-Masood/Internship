from turtle import Turtle
import random


class Food(Turtle):

    def __init__(self, boundary_x=280, boundary_y=280):
        super().__init__()
        self.boundary_x = boundary_x
        self.boundary_y = boundary_y
        self.shape("circle")
        self.penup()
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.color("blue")
        self.speed("fastest")
        self.refresh()

    def refresh(self):
        """Move the food to a new random position within the playable area."""
        random_x = random.randint(int(-self.boundary_x), int(self.boundary_x))
        random_y = random.randint(int(-self.boundary_y), int(self.boundary_y))
        self.goto(random_x, random_y)
