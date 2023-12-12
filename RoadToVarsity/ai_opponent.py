import math
import random
from fsm import FSM

# Constants
WIDTH, HEIGHT = 600, 800

class AI:
    def __init__(self, name, racquet, ball, box, error, out_func):
        self.name = name
        self.racquet = racquet
        self.ball = ball
        self.box = box
        self.error = error
        self.out_func = out_func

        self.fsm = FSM("middle moving")
        self.init_fsm()
    
    def init_fsm(self):
        # Ball moving towards ai
        self.fsm.add_transition("towards", "to ball", self.move_towards_ball)
        self.fsm.add_transition("towards", "middle moving", self.move_towards_ball, "to ball")

        # Ball moving away from ai
        self.fsm.add_transition("away", "middle moving", self.move_towards_middle)

        # Start of point
        self.fsm.add_transition("serving", "middle moving", self.move_towards_middle)

        # ai hits ball, then starts go back to middle
        self.fsm.add_transition("ai hit", "to ball", self.random_hit, "middle moving")
        self.fsm.add_transition("player hit", "middle moving", self.move_towards_middle)

    # Basic function for moving the AI
    def move(self):
        self.racquet.x += self.racquet.speed * self.direction[0]
        self.racquet.y += self.racquet.speed * self.direction[1]
        
    # ChatGPT generated and edited by Derek Jain
    def move_towards_ball(self):
        angle = math.atan2(self.ball.y - self.racquet.y, self.ball.x - self.racquet.x)
        self.direction = [math.cos(angle), math.sin(angle)]
        # Move the AI near the ball once the ball is hit, make sure the AI can't cross the the line
        if self.racquet.y < HEIGHT // 2 - self.racquet.height and self.ball.y < (HEIGHT // 2 - self.ball.radius) + 100:
            self.move()
        elif self.ball.y < HEIGHT // 2 - self.ball.radius:
            self.racquet.y -= self.racquet.speed * abs(self.direction[1])

    def move_towards_middle(self):
        target_x = WIDTH // 2  - (.5 * self.racquet.width)
        target_y = 100 + (-.5 * self.racquet.height)
        if (self.racquet.x <= target_x + 5 and self.racquet.x >= target_x - 5) and (self.racquet.y <= target_y + 5 and self.racquet.y >= target_y - 5):
            self.racquet.x = target_x
            self.racquet.y = target_y
            self.direction = [0,0]
        else:  
             # Move towards the top middle of the screen
            angle = math.atan2(target_y - self.racquet.y, target_x - self.racquet.x)
            self.direction = [math.cos(angle), math.sin(angle)]
            self.move()
    # End of ChatGPT code
    
    def random_hit(self):
        click_x = random.uniform(self.box.left - self.error, self.box.right + self.error)
        click_y = random.uniform(self.box.top - self.error, self.box.bottom + self.error)
        self.out_func(click_x, click_y)

    def update(self, ball_state):
        self.fsm.process(ball_state)