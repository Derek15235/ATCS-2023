import random
import math


class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.added_speed = 0
        self.direction = [random.choice([.1, -.1, .2, -.2, .3, -.3, .4, -.4, -.5, .5]), random.choice([.1, -.1, .2, -.2, .3, -.3, .4, -.4, -.5, .5])]

    def move(self):
        self.x += (self.speed + self.added_speed) * self.direction[0]
        self.y += (self.speed + self.added_speed) * self.direction[1]
    
    def move_towards(self, target_x, target_y):
        angle = math.atan2(target_y - self.y, target_x - self.x)
        self.direction = [math.cos(angle), math.sin(angle)]