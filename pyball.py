import pygame
import sys
import time

WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH,HEIGHT))

BLACK = (0,0,0)


class Block:

    def __init__(self, pos=(0,0)):
        self.pos = pygame.Vector2(pos)
        self.width = 25
        self.height = 100
        self.color = (255,255,255)
        self.speed = 3.0

        # Rect Controller
        self.block_controller = pygame.Rect(pos[0], pos[1], self.width, self.height)
        # Display Rect
        self.block = pygame.draw.rect(screen, self.color, self.block_controller)

    def move(self, dir):
        self.pos = self.pos + dir * self.speed

        self.block_controller = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def draw(self):
        self.block = pygame.draw.rect(screen, self.color, self.block_controller)

class Ball:
    
    def __init__(self, pos=(0,0), speed=5.0):
        self.pos = pygame.Vector2(pos)
        self.size = 15
        self.color = (255,255,255)
        self.speed = speed
        self.x_dir = 1
        self.y_dir = -1

        # Ball Controller
        self.block_controller = pygame.Rect(pos[0], pos[1], self.size, self.size)
        # Display Ball
        self.block = pygame.draw.rect(screen, self.color, self.block_controller)

    def move(self):
        self.pos[0] += self.speed * self.x_dir
        self.pos[1] += self.speed * self.y_dir

        self.block_controller = pygame.Rect(self.pos[0], self.pos[1], self.size, self.size)

    def draw(self):
        self.block = pygame.draw.rect(screen, self.color, self.block_controller)

    def reset(self):
        self.pos[0] = WIDTH//2
        self.pos[1] = HEIGHT//2
        


def main():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()
    speed_multiplier = 3
    dt = 0

    # Window Title
    pygame.display.set_caption("PyBall: Retro Edition")

    # Create Player
    player = Block(pos=(WIDTH//16,HEIGHT//2))

    # Create AI
    comp = Block(pos=(WIDTH - WIDTH//16 - player.width, HEIGHT//2))

    # Create Ball
    ball = Ball(pos=(WIDTH//2, HEIGHT//2))

    def Default_Positions():
        ball.reset()
        player.pos = (WIDTH//16,HEIGHT//2)
        comp.pos = (WIDTH - WIDTH//16 - player.width, HEIGHT//2)


    # Game loop to keep the window open
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        # Keybinds
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.pos[1] > 2:
            player.move(pygame.Vector2(0, -1.5*speed_multiplier))
        if keys[pygame.K_DOWN] and player.pos[1] < HEIGHT-player.height-2:
            player.move(pygame.Vector2(0, 1.5*speed_multiplier))

        # Edge detection
        if ball.pos[1] <= 0 or ball.pos[1] >= HEIGHT - ball.size:
            ball.y_dir *= -1
        if ball.pos[0] >= WIDTH:
            time.sleep(1)
            Default_Positions()
        elif ball.pos[0] <= 0 - ball.size:
            Default_Positions()
        ball.move()
            
        player.draw()
        comp.draw()
        ball.draw()
        # Update display
        pygame.display.flip()
        dt = clock.tick(30)

if __name__ == "__main__":
    main()