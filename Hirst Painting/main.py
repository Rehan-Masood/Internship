import turtle as turtle_module
import random

color_list = [
    (202, 164, 109),
    (238, 240, 245),
    (150, 75, 49),
    (223, 201, 135),
    (52, 93, 124),
    (172, 154, 40),
    (140, 30, 19),
    (2, 32, 61),
    (140, 137, 132),
    (28, 88, 90),
]

turtle_module.colormode(255)
tim = turtle_module.Turtle()
tim.speed("fastest")
tim.penup()
tim.hideturtle()

tim.setheading(225)
tim.forward(300)
tim.setheading(0)

number_of_dots = 100
dot_spacing = 50

for dot_count in range(1, number_of_dots + 1):
    tim.dot(20, random.choice(color_list))
    tim.forward(dot_spacing)

    if dot_count % 10 == 0:
        tim.setheading(90)
        tim.forward(dot_spacing)
        tim.setheading(180)
        tim.forward(dot_spacing * 10)
        tim.setheading(0)

screen = turtle_module.Screen()
screen.exitonclick()
