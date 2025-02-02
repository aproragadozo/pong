import random
import sys
import pygame
import pygame_widgets
import pygame_menu
from pygame_widgets.button import Button


pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

# Screen setup (is moved into main(), and passed on to the two subscreens)
screen_info = pygame.display.Info()
INITIAL_WIDTH = screen_info.current_w
INITIAL_HEIGHT = screen_info.current_h - 40 #room for title bar!
# SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN.get_size()
target_score = 10

# font as surface to render
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
bg_color = pygame.Color('#2F373F')
accent_color = (27,35,43)
# I'll put this back in later
# middle_strip = pygame.Rect(SCREEN_WIDTH/2 - 2,0,4,SCREEN_HEIGHT)

# Paddle properties as percentages of screen
PADDLE_WIDTH_PERCENT = 0.016  # roughly 15px on a 900px wide screen
PADDLE_HEIGHT_PERCENT = 0.15  # roughly 90px on a 600px high screen
PADDLE_OFFSET_PERCENT = 0.055  # roughly 50px on a 900px wide screen
PADDLE_SPEED_PERCENT = 0.008  # scales with screen height

# Ball properties
BALL_SIZE_PERCENT = 0.025  # scales with screen width
BALL_SPEED_X_PERCENT = 0.006
BALL_SPEED_Y_PERCENT = 0.006

class Paddle:
    def __init__(self, x_percent, screen_width, screen_height):
        self.x_percent = x_percent
        self.update_dimensions(screen_width, screen_height)
        
    def update_dimensions(self, screen_width, screen_height):
        paddle_width = int(screen_width * PADDLE_WIDTH_PERCENT)
        paddle_height = int(screen_height * PADDLE_HEIGHT_PERCENT)
        x = int(screen_width * self.x_percent)
        y = screen_height//2 - paddle_height//2
        self.rect = pygame.Rect(x, y, paddle_width, paddle_height)
        self.speed = int(screen_height * PADDLE_SPEED_PERCENT)
        
    def move(self, up=True, screen_height=INITIAL_HEIGHT):
        if up and self.rect.top > 0:
            self.rect.y -= self.speed
        elif not up and self.rect.bottom < screen_height:
            self.rect.y += self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.reset()
        
    def reset(self):
        ball_size = int(self.screen_width * BALL_SIZE_PERCENT)
        self.rect = pygame.Rect(
            self.screen_width//2 - ball_size//2,
            self.screen_height//2 - ball_size//2,
            ball_size, ball_size
        )
        self.speed_x = int(self.screen_width * BALL_SPEED_X_PERCENT) * random.choice([-1, 1])
        self.speed_y = int(self.screen_height * BALL_SPEED_Y_PERCENT) * random.choice([-1, 1])
        
    def update_dimensions(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        ball_size = int(screen_width * BALL_SIZE_PERCENT)
        self.rect.width = ball_size
        self.rect.height = ball_size
        
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
        
    def bounce_y(self):
        self.speed_y *= -1
        
    def bounce_x(self):
        self.speed_x *= -1

def set_target_score(value):
    target_score = value

def main():
    screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Pong")
    while True:
        screen.fill(BLACK)
        screen_width, screen_height = screen.get_size()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(
            screen, screen_width//2 - 150, screen_height//2 - 250, 300, 100,
            text="Play", fontSize=45, margin=20,
            inactiveColour=(255,0,0), pressedColour=(0,255,0),
            radius=20, onClick=lambda: play(screen, target_score)
        )
        OPTIONS_BUTTON = Button(
            screen, screen_width//2 - 50, screen_height//2 - 250, 300, 100,
            text="Options", fontSize=45, margin=20,
            inactiveColour=(255,0,0), pressedColour=(0,255,0),
            radius=20, onClick=lambda: options(screen, target_score)
        )
        """
        button = Button(
            screen, screen_width//2 - 150, screen_height//2 - 250, 300, 500,
            text="Play", fontSize=45, margin=20,
            inactiveColour=(255,0,0), pressedColour=(0,255,0),
            radius=20, onClick=lambda: play(screen, points_to_win)
        )
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        pygame_widgets.update(events)
        pygame.display.flip()

def options(screen, target_score):
    while True:
        screen_width, screen_height = screen.get_size()
        screen.fill(BLACK)
        ten = Button(
            screen, screen_width//2 - 300, screen_height//2 - 250, 300, 100,
            text='10',
            fontSize=45, margin=20,
            inactiveColour=(255,0,0), pressedColour=(0,255,0),
            radius=20, onClick=lambda: play(screen, 10)
        )
        fifteen = Button(
            screen, screen_width//2 - 400, screen_height//2 - 250, 300, 100,
            text='15',
            fontSize=45, margin=20,
            inactiveColour=(255,0,0), pressedColour=(0,255,0),
            radius=20, onClick=lambda: play(screen, 15)
        )
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        pygame_widgets.update(events)
        pygame.display.flip()

def end(winner, screen):
    while True:
        screen_width, screen_height = screen.get_size()
        screen.fill(BLACK)
        button = Button(
            screen, screen_width//2 - 300, screen_height//2 - 250, 600, 500,
            text=f"Congrats, {winner}, you win!",
            fontSize=45, margin=20,
            inactiveColour=(255,0,0), pressedColour=(0,255,0),
            radius=20, onClick=lambda: main()
        )
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        pygame_widgets.update(events)
        pygame.display.flip()

def play(screen, target_score):
    clock = pygame.time.Clock()
    screen_width, screen_height = screen.get_size()
    
    # Create paddles with percentage-based positioning
    left_paddle = Paddle(PADDLE_OFFSET_PERCENT, screen_width, screen_height)
    right_paddle = Paddle(1 - PADDLE_OFFSET_PERCENT - PADDLE_WIDTH_PERCENT, screen_width, screen_height)
    
    # Create ball
    ball = Ball(screen_width, screen_height)
    
    # Scores
    left_score = 0
    right_score = 0
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        current_width, current_height = screen.get_size()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                screen_width, screen_height = screen.get_size()
                # Update paddle and ball dimensions
                left_paddle.update_dimensions(screen_width, screen_height)
                right_paddle.update_dimensions(screen_width, screen_height)
                ball.update_dimensions(screen_width, screen_height)
                
        # Paddle control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move(up=True, screen_height=screen_height)
        if keys[pygame.K_s]:
            left_paddle.move(up=False, screen_height=screen_height)
        if keys[pygame.K_UP]:
            right_paddle.move(up=True, screen_height=screen_height)
        if keys[pygame.K_DOWN]:
            right_paddle.move(up=False, screen_height=screen_height)
            
        # Ball movement
        ball.move()
        
        # Ball collision with walls
        if ball.rect.top <= 0 or ball.rect.bottom >= screen_height:
            ball.bounce_y()
            
        # Ball collision with paddles
        if ball.rect.colliderect(left_paddle.rect) or ball.rect.colliderect(right_paddle.rect):
            ball.bounce_x()
            
        # Scoring
        if ball.rect.left <= 0:
            right_score += 1
            if right_score == target_score:
                end("Right player", screen)
            ball = Ball(screen_width, screen_height)
        if ball.rect.right >= screen_width:
            left_score += 1
            if left_score == target_score:
                end("Left player", screen)
            ball = Ball(screen_width, screen_height)
            
        # Drawing
        screen.fill(bg_color)
        pygame.draw.rect(screen, accent_color, pygame.Rect(screen_width/2 - 2, 0, 4, screen_height))
        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)
        
        # Draw scores
        left_text = font.render(str(left_score), True, WHITE)
        right_text = font.render(str(right_score), True, WHITE)
        
        # Get the size of the rendered text
        left_text_rect = left_text.get_rect()
        right_text_rect = right_text.get_rect()
        
        # Position text close to center stripe
        left_text_rect.center = (screen_width//2 - 30, screen_height//2)
        right_text_rect.center = (screen_width//2 + 30, screen_height//2)
        
        screen.blit(left_text, left_text_rect)
        screen.blit(right_text, right_text_rect)
        
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
