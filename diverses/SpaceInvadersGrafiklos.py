
import math
import random

# Score
score = 0


# Create the player
class Objekt:
    def __init__(self):
        self.posx = 0
        self.posy = 0

    def setposition(self, x, y):
        self.posx = x
        self.posy = y

    def xcor(self):
        return self.posx

    def ycor(self):
        return self.posy

    def setx(self, x):
        self.posx =x

    def sety(self, y):
            self.posx = y


player = Objekt()
player.setposition(0, -250)
enemy = Objekt()
playerspeed = 15

# Choose a number of enemies
number_of_enemies = 5
# Create an empty list of enemies
enemies = []
# Add enemies to list
for i in range(number_of_enemies):
    # Create an enemy
    enemies.append(enemy)
for enemy in enemies:
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

enemyspeed = 2

# Create a bullet
bullet = Objekt()
bullet.setposition(-2000, +2000)

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

# Main game loop

while True:


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



            # Check for collision between enemy and player
        if enemy.ycor() < player.ycor():

            print("Game Over")
            break

    # Move the bullet
    y = bullet.ycor()
    if y < 280:
        y += bulletspeed
        bullet.sety(y)
    else:
        bullet.setx(2000)


# Code from Christian Thompson (adapted)
# UNFINISHED
