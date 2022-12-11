
import turtle


class Spielausgabe:
    def __init__(self, xSpieler, ySpieler):
        #Screen
        self.wn = turtle.Screen()
        self.wn.bgcolor("black")
        self.wn.title("Space Invaders")
        self.wn.tracer(6)


        self.border_pen = turtle.Turtle()
        self.border_pen.speed(0)
        self.border_pen.color("white")
        self.border_pen.penup()
        self.border_pen.setposition(-300, -300)
        self.border_pen.pendown()
        self.border_pen.pensize(3)
        for side in range(4):
            self.border_pen.fd(600)
            self.border_pen.lt(90)
        self.border_pen.hideturtle()

        # Score

        self.score_pen = turtle.Turtle()
        self.score_pen.speed(0)
        self.score_pen.color("white")
        self.score_pen.penup()
        self.score_pen.setposition(-290, 280)
        self.scorestring = "Score: %s" % 0
        self.score_pen.write(self.scorestring, False, align="left", font=("Arial", 10, "normal"))
        self.score_pen.hideturtle()

        # Generation
        self.generation_pen = turtle.Turtle()
        self.generation_pen.speed(0)
        self.generation_pen.color("white")
        self.generation_pen.penup()
        self.generation_pen.setposition(210, 280)
        self.genstring = "Generation: %s" % 0
        self.generation_pen.write(self.genstring, False, align="left", font=("Arial", 10, "normal"))
        self.generation_pen.hideturtle()
        # Draw Border

        
        # Create the player turtle
        self.player = turtle.Turtle()
        self.player.color("blue")
        self.player.shape("triangle")
        self.player.penup()
        self.player.speed(0)
        self.player.setposition(xSpieler, ySpieler)
        self.player.setheading(90)
        
        

        # Create an empty list of enemies
        self.enemies = []
        # Add enemies to list
            # Siehe gegnerezeugen

        

        # Create a bullet
        self.bullet = turtle.Turtle()
        self.bullet.shape("triangle")
        self.bullet.color("yellow")
        self.bullet.penup()
        self.bullet.speed(0)
        self.bullet.shapesize(0.5, 0.5)
        self.bullet.setposition(-2000, +2000)
        self.bullet.setheading(90)



    def gegnererzeugen(self, x: int, y: int):
        enemy = turtle.Turtle()
        enemy.shape("circle")
        enemy.color("red")
        enemy.penup()
        enemy.speed(0)
        enemy.setposition(x, y)

        self.enemies.append(enemy)
        self.wn.update()

        # Main game loop
        
    def aktualisiern(self, bulletx, bullety, score, gegnerliste: list, spielerx, bulletstate, generation: int):
        # player
        self.player.setx(spielerx)
        # enemies

        for i in range(0, len(gegnerliste)):
            x = gegnerliste[i].xGeben()
            y = gegnerliste[i].yGeben()
            self.enemies[i].setposition(x,y)
        for j in range(len(gegnerliste),len(self.enemies)):
            self.enemies[j].setposition(500,-500)

        #bullet
        if bulletstate == "abgefeuert":
            self.bullet.showturtle()
            self.bullet.setx(bulletx)
            self.bullet.sety(bullety)
        else:
            self.bullet.hideturtle()
        #score
        self.scorestring = "Score: %s" % score
        self.score_pen.clear()
        self.score_pen.write(self.scorestring, False, align="left", font=("Arial", 10, "normal"))
        self.wn.update()
        # Generation
        self.genstring = "Generation: %s" % generation
        self.generation_pen.clear()
        self.generation_pen.write(self.genstring, False, align="left", font=("Arial", 10, "normal"))
        
    def gegneraktualisieren(self, x, y, indexgegner):
        self.enemies[indexgegner].setx(x)
        self.enemies[indexgegner].sety(y)

    def spielerbewegen(self, x):
        self.player.setx(x)
    # Code from Christian Thompson (adapted)