import pygame

YELLOW = (255, 255, 0)

class HitBox:
    def __init__(self, x, y, width, height, duration):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.duration = duration
        self.timer = 0

    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, (self.x, self.y, self.width, self.height))

    def update(self):
        self.timer += 1
        return self.timer >= self.duration