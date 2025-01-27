import pygame
import random

pygame.init()

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle properties
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
PADDLE_SPEED = 5

# Ball properties
BALL_SIZE = 15
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

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
    clock = pygame.time.Clock()
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
            ball = Ball()
        if ball.rect.right >= SCREEN_WIDTH:
            left_score += 1
            ball = Ball()
        # Drawing
        screen.fill(BLACK)
        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)
        # Draw scores
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_text, (SCREEN_WIDTH//4, 20))
        screen.blit(right_text, (3*SCREEN_WIDTH//4, 20))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
