# Generated by ChatGPT and edited by Derek Jain
import pygame
import sys
import random
from ai_opponent import AI
from ball import Ball
from hit_box import HitBox
from racquet import Racquet

# Constants
WIDTH, HEIGHT = 600, 800
BALL_RADIUS = 8
RACQUET_WIDTH, RACQUET_HEIGHT = 100, 100
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEED_INCREASE = 2
POWER_INCREASE = 2
ERROR_DECREASE = 1.5

class Game:
    def __init__(self, width, height, player_speed, ai_speed, player_power, ai_power, ai_margin, game_number=1, total_scores={"AI":0, "player":0}):
        pygame.init()
        self.WIDTH = width
        self.HEIGHT = height
        self.court_width = width - 200
        self.court_height = height - 200
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Road to Varsity")

        # Load player images and scale them down
        self.ai_image = pygame.image.load("assets/AI.png")
        self.ai_image = pygame.transform.flip(self.ai_image, False, True)
        self.ai_image = pygame.transform.scale(self.ai_image, (int(RACQUET_WIDTH * 7 / 8), int(RACQUET_HEIGHT * 7 / 8)))

        self.player_image = pygame.image.load("assets/player.png")
        self.player_image = pygame.transform.scale(self.player_image, (int(RACQUET_WIDTH * 7 / 8), int(RACQUET_HEIGHT * 7 / 8)))

        # Load background image (scaled down)
        background_original = pygame.image.load("assets/tennis_court.png")
        background_original = pygame.transform.scale(background_original, (self.court_width, self.court_height))
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.background.blit(background_original, (100, 100))

        self.clock = pygame.time.Clock()
        self.hit_box = None
        self.collide = False
        self.current = None
        self.ball_state = "serving"
        self.player_hit_timer = 0
        self.total_scores = total_scores

        # Define designated placement boxes for each player
        self.ai_box = pygame.Rect(self.WIDTH// 4, self.HEIGHT// 2 , self.WIDTH// 2, self.court_height // 2)
        self.player_box = pygame.Rect(self.WIDTH // 4, 100, self.WIDTH // 2, self.court_height // 2)

        self.ball = Ball(width // 2, height // 2, BALL_RADIUS, 5)
        self.racquet_ai = Racquet(width // 2 - RACQUET_WIDTH // 2, 100 - RACQUET_HEIGHT * .5, RACQUET_WIDTH, RACQUET_HEIGHT, ai_speed, ai_power)
        # Change AI look based on current game/stage on
        self.game_number = game_number
        if self.game_number == 1:
            self.name = "Alex"
        elif self.game_number == 2:
            self.name = "Ralph"
        elif self.game_number == 3:
            self.name = "Octave"
        elif self.game_number == 4:
            self.name = "Adam"
        elif self.game_number == 5:
            self.name = "Yuri"

        self.ai_controller = AI(self.name, self.racquet_ai, self.ball, self.ai_box, ai_margin, self.out)

        self.racquet_player = Racquet(width // 2 - RACQUET_WIDTH // 2, height - RACQUET_HEIGHT * .5 - 100, RACQUET_WIDTH, RACQUET_HEIGHT, player_speed, player_power)

        # Scores for the game and set
        self.set = [0, 0]
        self.current_game_scores = [0, 0]

        # Delay variables
        self.delaying = True
        self.delay_timer = 0


        # Fonts
        self.font = pygame.font.Font(None, 36)
        # Add a font for displaying "OUT" message
        self.out_font = pygame.font.Font(None, 72)

         # Define designated boxes for each player
        self.ai_box = pygame.Rect(self.WIDTH// 4, self.HEIGHT// 2 , self.WIDTH// 2, self.court_height // 2)
        self.player_box = pygame.Rect(self.WIDTH // 4, 100, self.WIDTH // 2, self.court_height // 2)

    def out(self, x, y):
        if (self.current == "ai" and self.ai_box.collidepoint(x, y)) or (self.current == "player" and self.player_box.collidepoint(x, y)):
            self.hit_box = HitBox(x, y, 20, 20, 20)
            # Update ball speed based on the racquet power
            if self.current == "ai":
                self.ball.added_speed = self.racquet_ai.power
            else:
                self.ball.added_speed = self.racquet_player.power
        else:
            # Some altered/added code: hit box is drawn, displaying its out
            self.hit_box = HitBox(x, y, 20, 20, 120)
            self.hit_box.draw(self.screen)
            out_text = self.out_font.render("OUT", True, WHITE)
            self.screen.blit(out_text, (self.WIDTH // 2 - out_text.get_width() // 2, self.HEIGHT // 2 - out_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(1000)
            self.hit_box = None
            # If the player clicks out of bounds, then they have "missed"
            if self.current == "ai":
                self.current_game_scores[1] += 1
                self.total_scores["player"] += 1
            else:
                self.current_game_scores[0] += 1
                self.total_scores["AI"] += 1
            self.check_game_winner()
            self.reset_positions()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and self.hit_box is None and self.collide and self.current == "player":
                # Create a hit box at the mouse click position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.out(mouse_x, mouse_y)
                self.player_hit_timer = 0
                

    def update(self):
        keys = pygame.key.get_pressed()

        # Player movements
        if not self.delaying:
            if keys[pygame.K_a] and self.racquet_player.x > 0: 
                self.racquet_player.move_left()
            if keys[pygame.K_d] and self.racquet_player.x < self.WIDTH - self.racquet_player.width:
                self.racquet_player.move_right()
            if keys[pygame.K_w] and self.racquet_player.y > self.HEIGHT // 2:
                self.racquet_player.move_up()
            if keys[pygame.K_s] and self.racquet_player.y < self.HEIGHT - self.racquet_player.height:
                self.racquet_player.move_down()

        # Delay before each point
        if self.delaying:
            self.delay_timer += 1
            if self.delay_timer >= FPS * 2:  # 2 seconds delay
                self.delaying = False
                self.delay_timer = 0
                # Start moving the ball after the delay
                self.ball.direction = [random.choice([.1, -.1, .2, -.2, .3, -.3, .4, -.4, -.5, .5]), random.choice([.1, -.1, .2, -.2, .3, -.3, .4, -.4, -.5, .5])]
        else:
            if self.ball_state == "player hit":
                self.player_hit_timer += 1
                if self.player_hit_timer >= FPS - 30:  # .5 seconds
                    self.current_game_scores[0] += 1
                    self.total_scores["AI"] += 1
                    self.check_game_winner()
                    self.reset_positions()

            # The hit box has been made, so ball should move towards it
            if self.hit_box and self.collide:
        
                # Move the ball towards the center of the hit box
                self.ball.move_towards(self.hit_box.x + self.hit_box.width / 2,
                                        self.hit_box.y + self.hit_box.height / 2)

                self.collide = False

            # Update and check if the yellow box duration has expired
            if self.hit_box and self.hit_box.update():
                self.hit_box = None

            self.ball.move()

            # Update the balls state
            if self.ball.direction[1] < 0:
                self.ball_state = "towards"
            elif self.ball.direction[1] > 0:
                self.ball_state = "away"
            
            # Move the racquet_ai based on AI logic
            self.ai_controller.update(self.ball_state) 

            # Ball collisions with paddles
            if (
                not self.hit_box
                and self.racquet_ai.x < self.ball.x < self.racquet_ai.x + self.racquet_ai.width
                and self.racquet_ai.y < self.ball.y < self.racquet_ai.y + self.racquet_ai.height
            ):
                # If the ball hits ai, change ball state to 
                self.ball.direction = [0, 0]
                self.ball_state = "ai hit"
                self.collide = True
                self.current = "ai"
            elif (
                not self.hit_box
                and self.racquet_player.x < self.ball.x < self.racquet_player.x + self.racquet_player.width
                and self.racquet_player.y < self.ball.y < self.racquet_player.y + self.racquet_player.height
            ):
                # If the ball hits player, stop the ball and wait for a click
                self.ball.direction = [0, 0]
                self.ball_state = "player hit"
                self.collide = True
                self.current = "player"

            # Ball out of bounds
            if self.ball.y <= 0:
                self.current_game_scores[1] += 1
                self.total_scores["player"] += 1
                self.check_game_winner()
                self.reset_positions()
            elif self.ball.y >= self.HEIGHT - self.ball.radius:
                self.current_game_scores[0] += 1
                self.total_scores["AI"] += 1
                self.check_game_winner()
                self.reset_positions()
            elif (self.ball.x <= 0 or self.ball.x >= self.WIDTH - self.ball.radius) and self.ball.y <= self.HEIGHT // 2 - self.ball.radius:
                self.current_game_scores[1] += 1
                self.total_scores["player"] += 1
                self.check_game_winner()
                self.reset_positions()
            elif (self.ball.x <= 0 or self.ball.x >= self.WIDTH - self.ball.radius) and self.ball.y >= HEIGHT // 2 - self.ball.radius:
                self.current_game_scores[0] += 1
                self.total_scores["AI"] += 1
                self.check_game_winner()
                self.reset_positions()

    def check_game_winner(self):
        # Check if a game in the set is won
        if max(self.current_game_scores) >= 4:
            # Update the total game scores and reset the current game scores
            if self.current_game_scores[0] > self.current_game_scores[1]:
                self.set[0] += 1
                self.current_game_scores[0] = 0
                self.current_game_scores[1] = 0
            else:
                self.set[1] += 1
                self.current_game_scores[0] = 0
                self.current_game_scores[1] = 0

            # If a person reaches 6 games, the set ends (adjust this for the matches to go faster)
            if max(self.set) >= 6:
                 # Fill the screen with a background color
                self.screen.fill(BLACK)

                # Display the winner and quit thew application
                if self.set.index(max(self.set)) == 0:
                    winner_text = f"{self.ai_controller.name} is the winner!"
                else:
                    winner_text = f"You are the winner!"

                winner_font = pygame.font.Font(None, 72)
                winner_surface = winner_font.render(winner_text, True, WHITE)
                self.screen.blit(winner_surface, (self.WIDTH // 2 - winner_surface.get_width() // 2, self.HEIGHT // 2 - winner_surface.get_height() // 2))
                pygame.display.flip()
                pygame.time.delay(3000)  # Display the winner for 3 seconds
                
                # If you have played the total amount of matches needed to be evaluated, write in results + percentage of points won
                if self.game_number == 5:
                    self.screen.fill(BLACK)
                    percentage = 100.0 * (float(self.total_scores["player"]) / float(self.total_scores["AI"] + self.total_scores["player"]))
                    if self.total_scores["AI"] >= self.total_scores["player"]:
                        result_text = "You did not make Varsity!"
                    else:
                        result_text = "You made the team!"

                    # Displayt the result on the screen
                    result_font = pygame.font.Font(None, 65)
                    result_surface = result_font.render(result_text, True, WHITE)
                    self.screen.blit(result_surface, (self.WIDTH // 2 - result_surface.get_width() // 2, self.HEIGHT // 2 - result_surface.get_height() // 2))
                   
                    # Display the percentage text below the result text
                    percentage_text = f"Success Percentage: {percentage:.2f}%"
                    percentage_font = pygame.font.Font(None, 30)
                    percentage_surface = percentage_font.render(percentage_text, True, WHITE)
                    self.screen.blit(percentage_surface, (self.WIDTH // 2 - percentage_surface.get_width() // 2, self.HEIGHT // 2 + result_surface.get_height() // 2 + 10))

                    pygame.display.flip()
                    pygame.time.delay(3000)
                    sys.exit()
                else:
                    pygame.quit()
                    new_game = Game(self.WIDTH, self.HEIGHT, player_speed=self.racquet_player.speed, ai_speed=self.racquet_ai.speed + SPEED_INCREASE, player_power=self.racquet_player.power, ai_power=self.racquet_ai.power + POWER_INCREASE, ai_margin=self.ai_controller.error // ERROR_DECREASE, game_number=self.game_number + 1, total_scores=self.total_scores)
                    new_game.run()

            self.reset_positions()

            

    def reset_positions(self):
        self.racquet_ai.x = self.WIDTH // 2 - RACQUET_WIDTH // 2
        self.racquet_ai.y = 100 - RACQUET_HEIGHT * .5
        self.racquet_player.x = self.WIDTH // 2 - RACQUET_WIDTH // 2
        self.racquet_player.y = self.HEIGHT - RACQUET_HEIGHT * .5 - 100
        self.ball.x = self.WIDTH // 2
        self.ball.y = self.HEIGHT // 2
        self.ball.direction = [0, 0]  # Stop the ball initially
        self.current = None
        self.ball_state = "serving"
        self.ai_controller.fsm.current_state = "middle moving"
        self.ball.added_speed = 0
        self.player_hit_timer = 0  # Reset the player hit timer when resetting positions

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

        # Draw the game and set scores
        total_score_text = self.font.render(f"{self.set[0]} - {self.set[1]}", True, WHITE)
        self.screen.blit(total_score_text, (self.WIDTH // 2 - total_score_text.get_width() // 2, 20))

        # Draw the current game scores
        tennis_scores = {0: "0", 1: "15", 2: "30", 3: "40"}
        player1_tennis_score = tennis_scores[self.current_game_scores[0]]
        player2_tennis_score = tennis_scores[self.current_game_scores[1]]


        game_score_text = self.font.render(f"{player1_tennis_score} - {player2_tennis_score}", True, WHITE)
        self.screen.blit(game_score_text, (self.WIDTH // 2 - game_score_text.get_width() // 2, 50))


        # Draw the yellow box if it exists
        if self.hit_box:
            self.hit_box.draw(self.screen)

        # Update the display
        pygame.display.flip()

    def draw_start_screen(self, name):
        self.screen.fill(BLACK)
        opponent_name = name  # Replace with the appropriate opponent name
        opponent_font = pygame.font.Font(None, 50)
        opponent_surface = opponent_font.render(f"You are playing against {opponent_name}!", True, WHITE)
        self.screen.blit(opponent_surface, (self.WIDTH // 2 - opponent_surface.get_width() // 2, self.HEIGHT // 2 - opponent_surface.get_height() // 2))
        pygame.display.flip()

        # Record the start time
        start_time = pygame.time.get_ticks()

        while pygame.time.get_ticks() - start_time < 3000:
            # Keep updating the display during the delay
            self.handle_events()
            self.clock.tick(FPS)

    def run(self):
        self.draw_start_screen(self.name)
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game(WIDTH, HEIGHT, player_speed=5, ai_speed=5, player_power=4, ai_power=.5, ai_margin=40)
    game.run()

