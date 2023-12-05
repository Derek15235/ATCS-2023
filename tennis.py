import pygame
import sys
import random
import math

# Constants
WIDTH, HEIGHT = 600, 800
BALL_RADIUS = 8
RACQUET_WIDTH, RACQUET_HEIGHT = 80, 80
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

class Ball:
    def __init__(self, x, y, radius, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.direction = [random.choice([.1, -.1, .2, -.2, .3, -.3, .4, -.4, -.5, .5]), random.choice([.1, -.1, .2, -.2, .3, -.3, .4, -.4, -.5, .5])]

    def move(self):
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]
    
    def move_towards(self, target_x, target_y):
        angle = math.atan2(target_y - self.y, target_x - self.x)
        self.direction = [math.cos(angle), math.sin(angle)]


class Racquet:
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

class YellowBox:
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

    def is_ball_near(self, ball):
        # Calculate the distance between the center of the box and the ball
        distance = math.sqrt((self.x + self.width / 2 - ball.x) ** 2 + (self.y + self.height / 2 - ball.y) ** 2)
        return distance < BALL_RADIUS + max(self.width, self.height) / 2

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.WIDTH = width
        self.HEIGHT = height
        self.court_width = width - 200
        self.court_height = height - 200
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Vertical Tennis Game")

        # Load player images and scale them down
        self.ai_image = pygame.image.load("player1.png")
        self.ai_image = pygame.transform.scale(self.ai_image, (int(RACQUET_WIDTH * 7 / 8), int(RACQUET_HEIGHT * 7 / 8)))

        self.player_image = pygame.image.load("player2.png")
        self.player_image = pygame.transform.scale(self.player_image, (int(RACQUET_WIDTH * 7 / 8), int(RACQUET_HEIGHT * 7 / 8)))

        # Load background image (scaled down)
        background_original = pygame.image.load("tennis_court.png")
        background_original = pygame.transform.scale(background_original, (self.court_width, self.court_height))
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.blit(background_original, (100, 100))

        self.clock = pygame.time.Clock()
        self.yellow_box = None
        self.hit_player = False
        self.current = None

        self.ball = Ball(width // 2, height // 2, BALL_RADIUS, 5)
        self.racquet_ai = Racquet(width // 2 - RACQUET_WIDTH // 2, 0, RACQUET_WIDTH, RACQUET_HEIGHT, 10)
        self.racquet_player = Racquet(width // 2 - RACQUET_WIDTH // 2, height - RACQUET_HEIGHT, RACQUET_WIDTH, RACQUET_HEIGHT, 10)

        self.score = [0, 0]

        # Delay variables
        self.delaying = False
        self.delay_timer = 0


        # Fonts
        self.font = pygame.font.Font(None, 36)

         # Define designated boxes for each player
        self.ai_box = pygame.Rect(self.WIDTH// 4, self.HEIGHT// 2 , self.WIDTH// 2, self.court_height // 2)
        self.player_box = pygame.Rect(self.WIDTH // 4, 100, self.WIDTH // 2, self.court_height // 2)
        # Colors
        self.GREEN = (0, 255, 0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.yellow_box is None and self.hit_player:
                # Create a yellow box at the mouse click position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if (self.current == "ai" and self.ai_box.collidepoint(mouse_x, mouse_y)) or (self.current == "player" and self.player_box.collidepoint(mouse_x, mouse_y)):
                    self.yellow_box = YellowBox(mouse_x, mouse_y, 20, 20, 120)
                else:
                    # Some altered/added code: yellow box is drawn, displaying its out
                    self.yellow_box = YellowBox(mouse_x, mouse_y, 20, 20, 120)
                    self.yellow_box.draw(self.screen)
                    pygame.display.flip()
                    pygame.time.delay(1000)
                    self.yellow_box = None
                    if self.current == "ai":
                        self.score[1] += 1
                    else:
                        self.score[0] += 1
                    self.reset_positions()

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.racquet_ai.x > 0:
            self.racquet_ai.move_left()
        if keys[pygame.K_RIGHT] and self.racquet_ai.x < self.WIDTH - self.racquet_ai.width:
            self.racquet_ai.move_right()
        if keys[pygame.K_UP] and self.racquet_ai.y > 0:
            self.racquet_ai.move_up()
        if keys[pygame.K_DOWN] and self.racquet_ai.y < self.HEIGHT // 2 - self.racquet_ai.height:
            self.racquet_ai.move_down()

        if keys[pygame.K_a] and self.racquet_player.x > 0:
            self.racquet_player.move_left()
        if keys[pygame.K_d] and self.racquet_player.x < self.WIDTH - self.racquet_player.width:
            self.racquet_player.move_right()
        if keys[pygame.K_w] and self.racquet_player.y > self.HEIGHT // 2:
            self.racquet_player.move_up()
        if keys[pygame.K_s] and self.racquet_player.y < self.HEIGHT - self.racquet_player.height:
            self.racquet_player.move_down()

        if self.delaying:
            self.delay_timer += 1
            if self.delay_timer >= FPS * 2:  # 2 seconds delay
                self.delaying = False
                self.delay_timer = 0
                # Start moving the ball after the delay
                self.ball.direction = [random.choice([.1, -.1, .2, -.2, .3, -.3, .4, -.4, -.5, .5]), random.choice([.1, -.1, .2, -.2, .3, -.3, .4, -.4, -.5, .5])]

        else:
            if self.yellow_box and self.hit_player:
                
                # Move the ball towards the center of the yellow box
                self.ball.move_towards(self.yellow_box.x + self.yellow_box.width / 2,
                                        self.yellow_box.y + self.yellow_box.height / 2)

                self.hit_player = False

            # Check if the ball is near the yellow box and make it disappear
            if self.yellow_box and self.yellow_box.is_ball_near(self.ball):
                self.yellow_box = None

            # Update and check if the yellow box duration has expired
            if self.yellow_box and self.yellow_box.update():
                self.yellow_box = None

            self.ball.move()

            # Ball collisions with paddles
            if (
                not self.delaying
                and self.racquet_ai.x < self.ball.x < self.racquet_ai.x + self.racquet_ai.width
                and self.racquet_ai.y < self.ball.y < self.racquet_ai.y + self.racquet_ai.height
            ):
                # If the ball hits player1, stop the ball and wait for a click
                self.ball.direction = [0, 0]
                self.hit_player = True
                self.current = "ai"

            elif (
                not self.delaying
                and self.racquet_player.x < self.ball.x < self.racquet_player.x + self.racquet_player.width
                and self.racquet_player.y < self.ball.y < self.racquet_player.y + self.racquet_player.height
            ):
                # If the ball hits player2, stop the ball and wait for a click
                self.ball.direction = [0, 0]
                self.hit_player = True
                self.current = "player"

            # Ball out of bounds
            if self.ball.y <= 0:
                self.score[1] += 1
                self.reset_positions()
            elif self.ball.y >= self.HEIGHT - self.ball.radius:
                self.score[0] += 1
                self.reset_positions()
            elif (self.ball.x <= 0 or self.ball.x >= self.WIDTH - self.ball.radius) and self.ball.y <= self.HEIGHT // 2 - self.ball.radius:
                self.score[1] += 1
                self.reset_positions()
            elif (self.ball.x <= 0 or self.ball.x >= self.WIDTH - self.ball.radius) and self.ball.y >= HEIGHT // 2 - self.ball.radius:
                self.score[0] += 1
                self.reset_positions()
            

    def reset_positions(self):
        self.racquet_ai.x = self.WIDTH // 2 - RACQUET_WIDTH // 2
        self.racquet_ai.y = 0
        self.racquet_player.x = self.WIDTH // 2 - RACQUET_WIDTH // 2
        self.racquet_player.y = self.HEIGHT - RACQUET_HEIGHT
        self.ball.x = self.WIDTH // 2
        self.ball.y = self.HEIGHT // 2
        self.ball.direction = [0, 0]  # Stop the ball initially

        # Set a delay for 2 seconds
        self.delaying = True
        self.delay_timer = 0

    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))

        # Draw red borders around the screen
        pygame.draw.rect(self.screen, (255, 0, 0), (0, 0, self.WIDTH, 5))                   # Top border
        pygame.draw.rect(self.screen, (255, 0, 0), (0, self.HEIGHT - 5, self.WIDTH, 5))  # Bottom border
        pygame.draw.rect(self.screen, (255, 0, 0), (0, 0, 5, self.HEIGHT))                # Left border
        pygame.draw.rect(self.screen, (255, 0, 0), (self.WIDTH - 5, 0, 5, self.HEIGHT))  # Right border

        # Draw player images and ball
        self.screen.blit(self.ai_image, (self.racquet_ai.x, self.racquet_ai.y))
        self.screen.blit(self.player_image, (self.racquet_player.x, self.racquet_player.y))
        pygame.draw.circle(self.screen, WHITE, (int(self.ball.x), int(self.ball.y)), self.ball.radius)

        # Draw the score
        score_text = self.font.render(f"{self.score[0]} - {self.score[1]}", True, WHITE)
        self.screen.blit(score_text, (self.WIDTH // 2 - score_text.get_width() // 2, 20))

        # Draw the yellow box if it exists
        if self.yellow_box:
            self.yellow_box.draw(self.screen)

        # Draw green outlines for designated boxes
        pygame.draw.rect(self.screen, WHITE, self.ai_box, 2)
        pygame.draw.rect(self.screen, WHITE, self.player_box, 2)

        # Update the display
        pygame.display.flip()

    def run(self):
        show_initial_frame = True
        initial_frame_timer = 0

        while True:
            self.handle_events()

            if show_initial_frame:
                self.draw()
                initial_frame_timer += 1

                if initial_frame_timer >= FPS * 2:  # Pause for 2 seconds
                    show_initial_frame = False
                    initial_frame_timer = 0

            else:
                self.update()
                self.draw()
                self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT)
    game.run()

