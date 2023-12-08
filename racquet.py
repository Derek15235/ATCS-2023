

class Racquet:
    def __init__(self, x, y, width, height, speed, power):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.power = power

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed