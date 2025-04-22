import turtle
import time
import math
import random

screen = turtle.Screen()
screen.tracer(0)

deltaTime = 0
lastTime = 0
currentTime = 0

class Ball():
    def __init__(self):
        self.arrow = turtle.Turtle()
        self.arrow.speed(0)
        self.arrow.hideturtle()
        self.arrow.penup()

        self.dampening = 0.67
        self.friction = 0.97

        self.positionX = 0
        self.positionY = 0

        self.velocityX = 0
        self.velocityY = -4

        self.accelX = 0
        self.accelY = -4

        self.color = "blue"

    def Update(self):
        self.velocityX += self.accelX
        self.velocityY += self.accelY

        self.positionX += self.velocityX
        self.positionY += self.velocityY

        if (self.positionY < turtle.window_height() / -2 + 50):
            self.velocityY = -self.velocityY * self.dampening
            self.velocityX *= self.friction
            self.positionY = turtle.window_height() / -2 + 50
        elif (self.positionY > turtle.window_height() / 2 - 50):
            self.velocityY = -self.velocityY * self.dampening
            self.velocityX *= self.friction
            self.positionY = turtle.window_height() / 2 - 50

        if (self.positionX < turtle.window_width() / -2 + 50):
            self.velocityX = -self.velocityX * self.dampening
            self.velocityY *= self.friction
            self.positionX = turtle.window_width() / -2 + 50
        elif (self.positionX > turtle.window_width() / 2 - 50):
            self.velocityX = -self.velocityX * self.dampening
            self.velocityY *= self.friction
            self.positionX = turtle.window_width() / 2 - 50

    def Draw(self):
        self.arrow.clear()
        self.arrow.goto(self.positionX, self.positionY)
        self.arrow.dot(40, self.color)

ball1 = Ball()
ball1.color = "red"

balls = [ball1]

for i in range(6):
    balls.append(Ball())
    balls[i].positionX = random.randrange(turtle.window_width() / -2 + 50, turtle.window_width() / 2 + 50)

def distance(a, b):
    distanceX = abs(a.positionX - b.positionX)
    distanceY = abs(a.positionY - b.positionY)
    return math.sqrt(distanceX * distanceX + distanceY * distanceY)

def direction(x, y):
    magnitude = math.sqrt(x * x + y * y)
    if magnitude == 0:
        return 0, 0

    x /= magnitude
    y /= magnitude
    return x, y

def HandleCollision(a, b):
    distanceX = a.positionX - b.positionX
    distanceY = a.positionY - b.positionY

    dirX, dirY = direction(distanceX, distanceY)
    magnA, magnB = math.sqrt(a.velocityX * a.velocityX + a.velocityY * a.velocityY), math.sqrt(b.velocityX * b.velocityX + b.velocityY * b.velocityY)

    overlap = (40 + 0.5) - distance(a, b)
    if overlap > 0:
        dirX, dirY = direction(a.positionX - b.positionX, a.positionY - b.positionY)
        correction = overlap / 2  # split the push between both balls

        a.positionX += dirX * correction
        a.positionY += dirY * correction

        b.positionX -= dirX * correction
        b.positionY -= dirY * correction

    a.velocityX = dirX * a.dampening * magnB * 0.8
    a.velocityY = dirY * a.dampening * magnB * 0.8

    b.velocityX = -dirX * a.dampening * magnA * 0.8
    b.velocityY = -dirY * a.dampening * magnA * 0.8

def checkCollision(a, b):
    if (distance(a, b) < 40):
        HandleCollision(a, b)

def click(x, y):
    main_ball = balls[0]

    dirX = x - main_ball.positionX
    dirY = y - main_ball.positionY

    dirX, dirY = direction(dirX, dirY)

    speed = 90
    main_ball.velocityX = dirX * speed
    main_ball.velocityY = dirY * speed

def gameLoop():


    for i, FirstBall in enumerate(balls):
        for j in range(i + 1, len(balls)):
            SecondBall = balls[j]
            if FirstBall != SecondBall:
                checkCollision(FirstBall, SecondBall)

        FirstBall.Update()
        FirstBall.Draw()
        #FirstBall.accelX = (random.random() - 0.5) * 2
        #FirstBall.accelY = (random.random() - 0.5) * 2

    screen.update()
    screen.ontimer(gameLoop, 15)

gameLoop()
turtle.onscreenclick(click)


turtle.done()