import sys
from turtle import Screen
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

screen = Screen()
screen.setup(width=1.0, height=1.0)  
screen.bgcolor("black")
screen.title("My Snake Game")
screen.tracer(0)

window_width = screen.window_width()
window_height = screen.window_height()
wall_margin = 20  
boundary_x = window_width / 2 - wall_margin
boundary_y = window_height / 2 - wall_margin

snake = Snake()
food = Food(boundary_x, boundary_y)
scoreboard = Scoreboard(window_height)

screen.listen()
screen.onkey(snake.up, "Up")
screen.onkey(snake.down, "Down")
screen.onkey(snake.left, "Left")
screen.onkey(snake.right, "Right")

game_is_on = True
while game_is_on:
    screen.update()
    time.sleep(0.1)

    snake.move()

    if snake.head.distance(food) < 15:
        food.refresh()
        snake.extend()
        scoreboard.increase_score()

    if snake.head.xcor() > boundary_x or snake.head.xcor() < -boundary_x or \
            snake.head.ycor() > boundary_y or snake.head.ycor() < -boundary_y:
        game_is_on = False
        scoreboard.game_over()

    for segment in snake.segments[1:]:
        if snake.head.distance(segment) < 10:
            game_is_on = False
            scoreboard.game_over()

screen.exitonclick()
