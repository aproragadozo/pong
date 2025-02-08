import random
import sys
import pygame
import pygame_widgets
import pygame_menu
from pygame_widgets.button import Button

# sprite parent
class Block(pygame.sprite.Sprite):
    def __init__(self, path, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = (x_pos, y_pos))

class Player(Block):
    def __init__(self, path, x_pos, y_pos, speed, screen_height):
        super().__init__(path,x_pos,y_pos)
        self.speed = speed
        self.movement = 0
        self.screen_height = screen_height

    def screen_constrain(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height

    def update(self, ball_group):
        self.rect.y += self.movement
        self.screen_constrain()
        self.movement = 0

class Ball(Block):
    def __init__(self, path, x_pos, y_pos, speed_x, speed_y, paddles, screen_height, screen_width):
        super().__init__(path,x_pos,y_pos)
        self.speed_x = speed_x * random.choice((-1,1))
        self.speed_y = speed_y * random.choice((-1,1))
        self.paddles = paddles
        self.score_time = 0
        self.screen_height = screen_height
        self.screen_width = screen_width

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.collisions()
        
    def collisions(self):
        if self.rect.top <= 0 or self.rect.bottom >= self.screen_height:
            pygame.mixer.Sound.play(ping)
            self.speed_y *= -1

        if pygame.sprite.spritecollide(self,self.paddles,False):
            pygame.mixer.Sound.play(ping)
            collision_paddle = pygame.sprite.spritecollide(self,self.paddles,False)[0].rect
            if abs(self.rect.right - collision_paddle.left) < 10 and self.speed_x > 0:
                self.speed_x *= -1
            if abs(self.rect.left - collision_paddle.right) < 10 and self.speed_x < 0:
                self.speed_x *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 10 and self.speed_y < 0:
                self.rect.top = collision_paddle.bottom
                self.speed_y *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 10 and self.speed_y > 0:
                self.rect.bottom = collision_paddle.top
                self.speed_y *= -1

    def reset_ball(self):
        self.speed_x *= random.choice((-1,1))
        self.speed_y *= random.choice((-1,1))
        self.rect.center = (self.screen_width/2, self.screen_height/2)
        pygame.mixer.Sound.play(score_sound)

class Opponent(Block):
    def __init__(self, path, x_pos, y_pos, speed, screen_height):
        super().__init__(path,x_pos,y_pos)
        self.speed = speed
        self.screen_height = screen_height

    def update(self, ball_group):
        if random.random() < 0.85:  # 85% chance to move (adds some randomness)
            if self.rect.top < ball_group.sprite.rect.y:
                self.rect.y += self.speed
            if self.rect.bottom > ball_group.sprite.rect.y:
                self.rect.y -= self.speed
        self.constrain()

    def constrain(self):
        if self.rect.top <= 0: self.rect.top = 0
        if self.rect.bottom >= self.screen_height: self.rect.bottom = self.screen_height

class GameManager:
    def __init__(self, ball_group, paddle_group, screen):
        self.player_score = 0
        self.opponent_score = 0
        self.ball_group = ball_group
        self.paddle_group = paddle_group
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

    def run_game(self, screen, target_score):
        # Drawing the game objects
        self.paddle_group.draw(self.screen)
        self.ball_group.draw(self.screen)

        # Updating the game objects
        self.paddle_group.update(self.ball_group)
        self.ball_group.update()
        self.reset_ball()
        self.draw_score()

        # Check for win condition
        if self.player_score >= target_score:
            end("Player", screen)
        elif self.opponent_score >= target_score:
            end("Opponent", screen)

    def reset_ball(self):
        if self.ball_group.sprite.rect.right >= self.screen_width:
            self.opponent_score += 1
            self.ball_group.sprite.reset_ball()
        if self.ball_group.sprite.rect.left <= 0:
            self.player_score += 1
            self.ball_group.sprite.reset_ball()

    def draw_score(self):
        player_score = get_font(40).render(str(self.player_score),True,accent_color)
        opponent_score = get_font(40).render(str(self.opponent_score),True,accent_color)

        player_score_rect = player_score.get_rect(midleft = (self.screen_width / 2 + 40,self.screen_height/2))
        opponent_score_rect = opponent_score.get_rect(midright = (self.screen_width / 2 - 40,self.screen_height/2))

        self.screen.blit(player_score,player_score_rect)
        self.screen.blit(opponent_score,opponent_score_rect)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

# sound
ping = pygame.mixer.Sound("assets/pong.ogg")
score_sound = pygame.mixer.Sound("assets/score.ogg")

clock = pygame.time.Clock()

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


def set_target_score(value):
    target_score = value

def main():
    screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Pong")
    while True:
        screen.fill(bg_color)
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
            screen, screen_width//2 - 150, screen_height//2 - 100, 300, 100,  # Shift down
            text="Options", fontSize=45, margin=20,
            inactiveColour=(255,0,0), pressedColour=(0,255,0),
            radius=20, onClick=lambda: options(screen, target_score)
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
    screen_width, screen_height = screen.get_size()
    
    # Game objects
    player = Player('assets/Paddle.png', screen_width - 20, screen_height/2, 5, screen_height)
    opponent = Opponent('assets/Paddle.png', 20, screen_height/2, 5, screen_height)
    paddle_group = pygame.sprite.Group()
    paddle_group.add(player)
    paddle_group.add(opponent)

    ball = Ball('assets/Ball.png', screen_width/2, screen_height/2, 4, 4, paddle_group, screen_height, screen_width)
    ball_sprite = pygame.sprite.GroupSingle()
    ball_sprite.add(ball)

    game_manager = GameManager(ball_sprite,paddle_group, screen)
    
    running = True
    while running:
        #current_width, current_height = screen.get_size()
        screen_width, screen_height = screen.get_size()

        screen.fill(bg_color)
        
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
        player.movement = 0
        keys = pygame.key.get_pressed()
        #if keys[pygame.K_w]:
            #left_paddle.move(up=True, screen_height=screen_height)
        #if keys[pygame.K_s]:
            #left_paddle.move(up=False, screen_height=screen_height)
        if keys[pygame.K_UP]:
            #right_paddle.move(up=True, screen_height=screen_height)
            player.movement = -player.speed
        if keys[pygame.K_DOWN]:
            #right_paddle.move(up=False, screen_height=screen_height)
            player.movement = player.speed
        
        #pygame.display.flip()
        #pygame.draw.rect(screen, accent_color, middle_strip)
        game_manager.run_game(screen, target_score)
        pygame.display.flip()
        clock.tick(120)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
