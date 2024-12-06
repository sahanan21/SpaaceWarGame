import os
import random
import turtle
import pygame  # Uncomment if using pygame for sounds

# Setup turtle environment
turtle.speed(0)
turtle.bgcolor("black")
turtle.title("SpaceWar")
turtle.ht()
turtle.bgpic("sakk.gif")
turtle.setundobuffer(1)
turtle.tracer(3)

class Sprite(turtle.Turtle):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(shape=spriteshape)
        self.speed(0)
        self.penup()
        self.color(color)
        self.goto(startx, starty)
        self.speed = 1
    def move(self):
        self.fd(self.speed)
        self.check_boundaries()

    def check_boundaries(self):
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)
        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)
        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)
        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

    def is_collision(self, other):
        return (self.xcor() >= (other.xcor() - 20) and
                self.xcor() <= (other.xcor() + 20) and
                self.ycor() >= (other.ycor() - 20) and
                self.ycor() <= (other.ycor() + 20))

class Player(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.6, stretch_len=1.1, outline=None)
        self.speed = 4  
        self.lives = 3

    def turn_left(self):
        self.lt(45)

    def turn_right(self):
        self.rt(45)

    def accelerate(self):
        self.speed += 1

    def decelerate(self):
        self.speed -= 1

class Enemy(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.speed = 6
        self.setheading(random.randint(0, 360))

class Ally(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.speed = 8
        self.setheading(random.randint(0, 360))

class Missile(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
        self.speed = 20
        self.status = "ready"
        self.goto(-1000, 1000)
        self.sound = pygame.mixer.Sound("mixkit-game-bomb-magic-explosion-2808.wav")  # Uncomment if using pygame

    def fire(self):
        if self.status == "ready":
            # Play Missile sound if using pygame
            self.sound.play()
            os.system("mixkit-game-bomb-magic-explosion-2808.mp3 &")  # Replace with appropriate sound command
            self.goto(player.xcor(), player.ycor())
            self.setheading(player.heading())
            self.status = "firing"

    def move(self):
        if self.status == "ready":
            self.goto(-1000, 1000)
        if self.status == "firing":
            self.fd(self.speed)
        if self.xcor() < -290 or self.xcor() > 290 or self.ycor() < -290 or self.ycor() > 290:
            self.goto(-1000, 1000)
            self.status = "ready"

class Particle(Sprite):
    def __init__(self, spriteshape, color, startx, starty):
        super().__init__(spriteshape, color, startx, starty)
        self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
        self.goto(-1000, -1000)
        self.frame = 0

    def explode(self, startx, starty):
        self.goto(startx, starty)
        self.setheading(random.randint(0, 360))
        self.frame = 1

    def move(self):
        if self.frame > 0:
            self.fd(10)
            self.frame += 1
        if self.frame > 15:
            self.frame = 0
            self.goto(-1000, -1000)

class Game:
    def __init__(self):
        self.level = 1
        self.score = 0
        self.state = "playing"
        self.pen = turtle.Turtle()
        self.lives = 3
        pygame.init()  # Uncomment if using pygame
        pygame.mixer.init()  # Uncomment if using pygame
        self.laser_sound = pygame.mixer.Sound("mixkit-game-bomb-magic-explosion-2808.wav")  # Uncomment if using pygame

    def draw_border(self):
        self.pen.speed(0)
        self.pen.color("White")
        self.pen.pensize(3)
        self.pen.penup()
        self.pen.goto(-300, 300)
        self.pen.pendown()
        for _ in range(4):
            self.pen.fd(600)
            self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()

    def show_status(self):
        self.pen.undo()
        msg = f"Score : {self.score}"
        self.pen.penup()
        self.pen.goto(-300, 310)
        self.pen.write(msg, font=("Arial", 16, "normal"))

# Create game objects
game = Game()
game.draw_border()
game.show_status()

player = Player("triangle", "violet", 0, 0)
missile = Missile("triangle", "yellow", 0, 0)

enemies = [Enemy("circle", "red", random.randint(-290, 290), random.randint(-290, 290)) for _ in range(6)]
allies = [Ally("square", "blue", random.randint(-290, 290), random.randint(-290, 290)) for _ in range(6)]

particles = [Particle("circle", "orange", 0, 0) for _ in range(20)]

# Keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()

# Main game loop
while True:
    turtle.update()
    player.move()
    missile.move()
    for enemy in enemies:
        enemy.move()
        if player.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            game.score -= 100
            game.show_status()

        if missile.is_collision(enemy):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            enemy.goto(x, y)
            missile.status = "ready"
            for particle in particles:
                particle.explode(missile.xcor(), missile.ycor())
            game.score += 100
            game.show_status()

    for ally in allies:
        ally.move()
        if missile.is_collision(ally):
            x = random.randint(-250, 250)
            y = random.randint(-250, 250)
            ally.goto(x, y)
            missile.status = "ready"
            game.score -= 50
            game.show_status()

    for particle in particles:
        particle.move()

turtle.done()
