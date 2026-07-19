from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 2  # cars get faster with every level
SPAWN_CHANCE = 6    # 1 in 6 chance of a new car appearing each loop


class CarManager:
    """Creates and moves the cars that the player must dodge."""

    def __init__(self):
        self.all_cars = []
        self.car_speed = STARTING_MOVE_DISTANCE

    def create_car(self):
        """Randomly spawns a new car on the right edge of the screen."""
        random_chance = random.randint(1, SPAWN_CHANCE)
        if random_chance == 1:
            new_car = Turtle("square")
            new_car.shapesize(stretch_wid=1, stretch_len=2)
            new_car.penup()
            new_car.color(random.choice(COLORS))
            random_y = random.randint(-250, 250)
            new_car.goto(300, random_y)
            self.all_cars.append(new_car)

    def move_cars(self):
        """Moves every car on screen to the left."""
        for car in self.all_cars:
            car.backward(self.car_speed)

    def level_up(self):
        """Increases the car speed to make the next level harder."""
        self.car_speed += MOVE_INCREMENT
