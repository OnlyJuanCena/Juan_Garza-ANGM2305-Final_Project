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
        self.width = 15
        self.height = 90
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
        self.x_dir = 1
        self.y_dir = -1

        # Ball Controller
        self.block_controller = pygame.Rect(pos[0], pos[1], self.size, self.size)
        # Display Ball
        self.block = pygame.draw.rect(screen, self.color, self.block_controller)

    def move(self, speed):
        self.pos[0] += speed * self.x_dir
        self.pos[1] += speed * self.y_dir

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
    player_score = 0
    comp_score = 0
    speed_multiplier = 3
    hit_sound = pygame.mixer.Sound("sfx/pong_hit.wav")
    point_sound = pygame.mixer.Sound("sfx/pong_point.wav")
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
        point_sound.play()


    # Game loop to keep the window open
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.pos[1] > 2:
            player.move(pygame.Vector2(0, -1.5))
        if keys[pygame.K_DOWN] and player.pos[1] < HEIGHT-player.height-2:
            player.move(pygame.Vector2(0, 1.5))

        # Block-hit detection
        if pygame.Rect.colliderect(player.block_controller, ball.block_controller):
            ball.x_dir *= -1
            print("Bazzinga")
            hit_sound.play()
        if pygame.Rect.colliderect(comp.block_controller, ball.block_controller):
            ball.x_dir *= -1
            print("Bazzinga")
            hit_sound.play()

        # Edge-hit detection
        if ball.pos[1] <= 0 or ball.pos[1] >= HEIGHT - ball.size:
            ball.y_dir *= -1

        if ball.pos[0] >= WIDTH:
            Default_Positions()
            time.sleep(1)
            speed_multiplier = 3
            player_score += 1
            print(f"Player score: {player_score}")
        elif ball.pos[0] <= 0 - ball.size:
            Default_Positions()
            time.sleep(1)
            speed_multiplier = 3
            comp_score += 1
            print(f"Comp score: {comp_score}")
        ball.move(speed_multiplier*1.3)

        # AI movement
        if (comp.pos[1] <= ball.pos[1] and comp.pos[1] < HEIGHT-player.height-2):
            comp.move(pygame.Vector2(0, 1.5))
            # print("moving down")
        if (comp.pos[1] >= ball.pos[1] and comp.pos[1] > 2):
            comp.move(pygame.Vector2(0, -1.5))
            # print("moving up")

        # Ball speed ramp
        speed_multiplier *= 1.0005
            
        player.draw()
        comp.draw()
        ball.draw()
        # Update display
        pygame.display.flip()
        dt = clock.tick(60)

if __name__ == "__main__":
    main()