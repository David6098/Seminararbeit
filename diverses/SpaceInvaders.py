import turtle
import math
import random

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.tracer(2)

# Score
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" % score
score_pen.write(scorestring, False, align="left", font=("Arial", 10, "normal"))
score_pen.hideturtle()

# Draw Border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = 15

# Choose a number of enemies
number_of_enemies = 5
# Create an empty list of enemies
enemies = []
# Add enemies to list
for i in range(number_of_enemies):
    # Create an enemy
    enemies.append(turtle.Turtle())
for enemy in enemies:
    enemy.shape("circle")
    enemy.color("red")
    enemy.penup()
    enemy.speed(0)
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

enemyspeed = 2

# Create a bullet
bullet = turtle.Turtle()
bullet.shape("triangle")
bullet.color("yellow")
bullet.penup()
bullet.speed(0)
bullet.shapesize(0.5, 0.5)
bullet.setposition(-2000, +2000)
bullet.setheading(90)

bulletspeed = 10


# Shoot the bullet

def shoot():
    x = player.xcor()
    if bullet.ycor() > 260:
        bullet.setx(x)
        bullet.sety(player.ycor() + 5)


# Check for collision

def isCollision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


# Move player to right and left

def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)


def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)


# Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(shoot, "Up")

# Main game loop

while True:

    wn.update()
    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)
        if x > 280:
            for e in enemies:
                y = e.ycor() - 40
                e.sety(y)
            enemyspeed *= -1
        if x < -280:
            enemyspeed *= -1
            for e in enemies:
                y = e.ycor() - 40
                e.sety(y)

            # Check for collision between bullet and enemy

        if isCollision(bullet, enemy):
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)
            bullet.setx(-2000)
            score += 1
            scorestring = "Score: %s" % score
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 10, "normal"))


            # Check for collision between enemy and player
        if enemy.ycor() < player.ycor():
            player.hideturtle()
            for e in enemies:
                e.hideturtle()
            print("Game Over")
            break

    # Move the bullet
    y = bullet.ycor()
    if y < 280:
        y += bulletspeed
        bullet.sety(y)
    else:
        bullet.setx(2000)

wn.exitonclick()

# Code from Christian Thompson (adapted)
