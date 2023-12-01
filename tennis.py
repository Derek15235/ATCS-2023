import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 600, 800
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 80, 80
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

    def move(self):
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]

    def bounce_horizontal(self):
        self.direction[0] = -self.direction[0]

    def bounce_vertical(self):
        self.direction[1] = -self.direction[1]

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def move_left(self):
        self.x -= self.speed

    def move_right(self):
        self.x += self.speed

    def move_up(self):
        self.y -= self.speed

    def move_down(self):
        self.y += self.speed

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.WIDTH = width
        self.HEIGHT = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Vertical Tennis Game")

        # Load player images
        self.player1_image = pygame.image.load("player1.png")
        self.player1_image = pygame.transform.scale(self.player1_image, (PADDLE_WIDTH, PADDLE_HEIGHT))

        self.player2_image = pygame.image.load("player2.png")
        self.player2_image = pygame.transform.scale(self.player2_image, (PADDLE_WIDTH, PADDLE_HEIGHT))

        self.clock = pygame.time.Clock()

        self.ball = Ball(width // 2, height // 2, BALL_RADIUS, 3)
        self.paddle1 = Paddle(width // 2 - PADDLE_WIDTH // 2, 0, PADDLE_WIDTH, PADDLE_HEIGHT, 5)
        self.paddle2 = Paddle(width // 2 - PADDLE_WIDTH // 2, height - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, 5)

        self.score = [0, 0]

        # Delay variables
        self.delaying = False
        self.delay_timer = 0

        # Fonts
        self.font = pygame.font.Font(None, 36)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.paddle1.x > 0:
            self.paddle1.move_left()
        if keys[pygame.K_RIGHT] and self.paddle1.x < self.WIDTH - self.paddle1.width:
            self.paddle1.move_right()
        if keys[pygame.K_UP] and self.paddle1.y > 0:
            self.paddle1.move_up()
        if keys[pygame.K_DOWN] and self.paddle1.y < self.HEIGHT // 2 - self.paddle1.height:
            self.paddle1.move_down()

        if keys[pygame.K_a] and self.paddle2.x > 0:
            self.paddle2.move_left()
        if keys[pygame.K_d] and self.paddle2.x < self.WIDTH - self.paddle2.width:
            self.paddle2.move_right()
        if keys[pygame.K_w] and self.paddle2.y > self.HEIGHT // 2:
            self.paddle2.move_up()
        if keys[pygame.K_s] and self.paddle2.y < self.HEIGHT - self.paddle2.height:
            self.paddle2.move_down()

        if self.delaying:
            self.delay_timer += 1
            if self.delay_timer >= FPS:  # 1 second delay
                self.delaying = False
                self.delay_timer = 0
        else:
            self.ball.move()

            # Ball collisions with walls
            if self.ball.x <= 0 or self.ball.x >= self.WIDTH - self.ball.radius:
                self.ball.bounce_horizontal()

            # Ball collisions with paddles
            if (
                not self.delaying
                and self.paddle1.y <= self.ball.y <= self.paddle1.y + self.paddle1.height
                and self.paddle1.x <= self.ball.x <= self.paddle1.x + self.paddle1.width
                and self.ball.y + self.ball.radius >= self.paddle1.y + self.paddle1.height
            ):
                self.ball.bounce_vertical()
                self.delaying = True

            elif (
                not self.delaying
                and self.paddle2.y <= self.ball.y <= self.paddle2.y + self.paddle2.height
                and self.paddle2.x <= self.ball.x <= self.paddle2.x + self.paddle2.width
                and self.ball.y - self.ball.radius <= self.paddle2.y
            ):
                self.ball.bounce_vertical()
                self.delaying = True

            # Ball out of bounds
            if self.ball.y <= 0:
                self.score[1] += 1
                self.reset_positions()
            elif self.ball.y >= self.HEIGHT - self.ball.radius:
                self.score[0] += 1
                self.reset_positions()

    def reset_positions(self):
        self.paddle1.x = self.WIDTH // 2 - PADDLE_WIDTH // 2
        self.paddle1.y = 0
        self.paddle2.x = self.WIDTH // 2 - PADDLE_WIDTH // 2
        self.paddle2.y = self.HEIGHT - PADDLE_HEIGHT
        self.ball.x = self.WIDTH // 2
        self.ball.y = self.HEIGHT // 2
        self.ball.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

    def draw(self):
        # Clear the screen
        self.screen.fill(BLACK)

        # Draw player images and ball
        self.screen.blit(self.player1_image, (self.paddle1.x, self.paddle1.y))
        self.screen.blit(self.player2_image, (self.paddle2.x, self.paddle2.y))
        pygame.draw.circle(self.screen, WHITE, (int(self.ball.x), int(self.ball.y)), self.ball.radius)

        # Draw the score
        score_text = self.font.render(f"{self.score[0]} - {self.score[1]}", True, WHITE)
        self.screen.blit(score_text, (self.WIDTH // 2 - score_text.get_width() // 2, 20))

        # Update the display
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    game.run()
