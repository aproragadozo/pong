import random
import sys
import pygame
import pygame_widgets
from pygame_widgets.button import Button

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

# Screen setup
SCREEN = pygame.display.set_mode((900,600), pygame.RESIZABLE)
pygame.display.set_caption("Pong")
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()


# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
bg_color = pygame.Color('#2F373F')
accent_color = (27,35,43)
middle_strip = pygame.Rect(SCREEN_WIDTH/2 - 2,0,4,SCREEN_HEIGHT)

# Paddle properties
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
PADDLE_SPEED = 5

# Ball properties
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

class Block(pygame.sprite.Sprite):
    pass
class Player(Block):
    pass

class Object(Block):
    pass
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= PADDLE_SPEED
        elif not up and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PADDLE_SPEED
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
    def bounce_y(self):
        self.speed_y *= -1
    def bounce_x(self):
        self.speed_x *= -1

def main():
    while True:
        SCREEN.fill(BLACK)
        button = Button(
            SCREEN, 100, 100, 300, 500, text="Play",
            fontSize=45, margin=20,
            inactiveColour=(255,0,0),
            pressedColour=(0,255,0), radius=20,
            onClick=lambda: play()
        )
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame_widgets.update(events)
        pygame.display.flip()

def end(winner):
    while True:
        SCREEN.fill(BLACK)
        button = Button(
            SCREEN, 100, 100, 600, 500, text=f"Congrats, {winner}, you win!",
            fontSize=45, margin=20,
            inactiveColour=(255,0,0),
            pressedColour=(0,255,0), radius=20,
            onClick=lambda: play()
        )
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame_widgets.update(events)
        pygame.display.flip()


def play():
    clock = pygame.time.Clock()
    SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
    # Create paddles
    left_paddle = Paddle(50, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2)
    right_paddle = Paddle(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2)
    # Create ball
    ball = Ball()
    # Scores
    left_score = 0
    right_score = 0
    font = pygame.font.Font(None, 36)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # Paddle control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move(up=True)
        if keys[pygame.K_s]:
            left_paddle.move(up=False)
        if keys[pygame.K_UP]:
            right_paddle.move(up=True)
        if keys[pygame.K_DOWN]:
            right_paddle.move(up=False)
        # Ball movement
        ball.move()
        # Ball collision with walls
        if ball.rect.top <= 0 or ball.rect.bottom >= SCREEN_HEIGHT:
            ball.bounce_y()
        # Ball collision with paddles
        if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
            ball.bounce_x()
        # Scoring
        if ball.rect.left <= 0:
            right_score += 1
            if right_score == 10:
                end("Right player")
            ball = Ball()
        if ball.rect.right >= SCREEN_WIDTH:
            left_score += 1
            if left_score == 10:
                end("Left player")
            ball = Ball()
        # Drawing
        SCREEN.fill(bg_color)
        left_paddle.draw(SCREEN)
        right_paddle.draw(SCREEN)
        ball.draw(SCREEN)
        # Draw scores
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        SCREEN.blit(left_text, (SCREEN_WIDTH//4, 20))
        SCREEN.blit(right_text, (3*SCREEN_WIDTH//4, 20))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
