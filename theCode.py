import turtle
import time
import math
import random
from math import hypot

numBalls = 6

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
        self.mass = 30

        self.positionX = 0
        self.positionY = 0

        self.velocityX = 0
        self.velocityY = 0

        self.accelX = 0
        self.accelY = 0

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
ball1.mass = 1000
ball1.color = "red"

balls = [ball1]

colors = ["red", "yellow", "orange"]

for i in range(numBalls):
    currentBallIDK = Ball()
    currentBallIDK.color = colors[random.randint(0, len(colors) - 1)]
    currentBallIDK.positionX = random.randrange(turtle.window_width() / -2 + 50, turtle.window_width() / 2 + 50)
    currentBallIDK.positionY = random.randrange(int(turtle.window_height() / -2 + 50), int(turtle.window_height() / 2 + 50))
    balls.append(currentBallIDK)

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

def findGravity(a: Ball, b: Ball):
    rSqr = (hypot(b.positionX - a.positionX, b.positionY - a.positionY)**2)
    rSqr=max(rSqr, 40)
    if rSqr == 0: rSqr = 1
    force = (a.mass*b.mass)/ rSqr
    dirX, dirY = direction(b.positionX - a.positionX, b.positionY - a.positionY)
    a.accelX += force * dirX / a.mass
    a.accelY += force * dirY / a.mass
    b.accelX += force * -dirX / b.mass
    b.accelY += force * -dirY / b.mass


# Fuck you
def HandleCollision(a, b):
    dx = a.positionX - b.positionX
    dy = a.positionY - b.positionY
    dist = math.hypot(dx, dy)

    if dist == 0:
        return  # Avoid division by zero

    # Normal vector
    nx = dx / dist
    ny = dy / dist

    # Relative velocity
    rvx = a.velocityX - b.velocityX
    rvy = a.velocityY - b.velocityY

    # Relative velocity along the normal
    velAlongNormal = rvx * nx + rvy * ny

    # Skip if velocities are separating
    if velAlongNormal > 0:
        return

    # Coefficient of restitution (bounciness)
    e = 0.6  # lower means less bouncy

    # Calculate impulse scalar
    j = -(1 + e) * velAlongNormal
    j /= 2  # equal mass

    # Apply impulse
    impulseX = j * nx
    impulseY = j * ny

    a.velocityX += impulseX
    a.velocityY += impulseY
    b.velocityX -= impulseX
    b.velocityY -= impulseY

    # Positional correction
    overlap = 40 - dist
    if overlap > 0:
        correction = overlap / 2
        a.positionX += nx * correction
        a.positionY += ny * correction
        b.positionX -= nx * correction
        b.positionY -= ny * correction

def checkCollision(a, b):
    if (distance(a, b) < 40):
        HandleCollision(a, b)

def click(x, y):
    main_ball = balls[0]

    dirX = x - main_ball.positionX
    dirY = y - main_ball.positionY

    speed = math.hypot(dirX, dirY) * 0.2

    dirX, dirY = direction(dirX, dirY)

    main_ball.velocityX = dirX * speed
    main_ball.velocityY = dirY * speed

def gameLoop():
    for ball in balls:
        ball.accelX = 0
        ball.accelY = 0

    for i, FirstBall in enumerate(balls):
        #for j in range(i + 1, len(balls)):
            #SecondBall = balls[j]
            #if FirstBall != SecondBall:
                #checkCollision(FirstBall, SecondBall)
        findGravity(FirstBall, balls[0])
        FirstBall.Update()
        FirstBall.Draw()
        #FirstBall.accelX = (random.random() - 0.5) * 2
        #FirstBall.accelY = (random.random() - 0.5) * 2

    screen.update()
    screen.ontimer(gameLoop, 4)

gameLoop()
turtle.onscreenclick(click)


turtle.done()