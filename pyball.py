import pygame
import sys
import time

WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH,HEIGHT))
BLACK = (0,0,0)
TEXT_SIZE = 36


class Block:

    def __init__(self, pos=(0,0),):
        self.pos = pygame.Vector2(pos)
        self.width = 5
        self.height = 90
        self.color = (255,255,255)
        self.speed = 3.0
        self.font = pygame.font.SysFont('arial', TEXT_SIZE)

        # Rect Controller
        self.block_controller = pygame.Rect(pos[0], pos[1], self.width, self.height)
        # Display Rect
        self.block = pygame.draw.rect(screen, self.color, self.block_controller)

    def move(self, dir):
        self.pos = self.pos + dir * self.speed

        self.block_controller = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def draw(self):
        self.block = pygame.draw.rect(screen, self.color, self.block_controller)

    def score(self, score_text, pos):
        score_text = self.font.render(score_text, True, self.color)
        screen.blit(score_text, (pos[0]- score_text.get_width()//2, 
                                pos[1] - score_text.get_height()//2))

        

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
    player_score, comp_score = 0,0
    speed_multiplier = 2

    # Set volume
    volume = 0.3
    hit_sound = pygame.mixer.Sound("sfx/pong_hit.wav")
    point_sound = pygame.mixer.Sound("sfx/pong_point.wav")
    pygame.mixer.Sound.set_volume(hit_sound, volume)
    pygame.mixer.Sound.set_volume(point_sound, volume)
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
        while player_score < 3 and comp_score < 3: # Number of rounds before end before winner
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

            # AI movement
            if (comp.pos[1] <= ball.pos[1] and comp.pos[1] < HEIGHT-comp.height-2):
                comp.move(pygame.Vector2(0, 1.5))
                # print("moving down")
            if (comp.pos[1] >= ball.pos[1] and comp.pos[1] > 2):
                comp.move(pygame.Vector2(0, -1.5))
                # print("moving up")


            # TODO: Fix ball collision glitch with player and comp

            # Player Block-hit detection
            if pygame.Rect.colliderect(player.block_controller, ball.block_controller):
                ball.x_dir *= -1
                if keys[pygame.K_UP]:
                    ball.y_dir = -1
                elif keys[pygame.K_DOWN]:
                    ball.y_dir = 1
                hit_sound.play()

            # Comp Block-hit detection
            if pygame.Rect.colliderect(comp.block_controller, ball.block_controller):
                ball.x_dir *= -1
                hit_sound.play()

            # Edge-hit detection
            if ball.pos[1] <= 0 or ball.pos[1] >= HEIGHT - ball.size:
                ball.y_dir *= -1

            if ball.pos[0] >= WIDTH: # right wall detection
                Default_Positions()
                time.sleep(1)
                speed_multiplier = 2
                player_score += 1
            elif ball.pos[0] <= 0 - ball.size: # left wall detection
                Default_Positions()
                time.sleep(1)
                speed_multiplier = 2
                comp_score += 1
            ball.move(speed_multiplier*1.3)

            # Ball speed ramp
            speed_multiplier *= 1.0005

            # Update display
            player.draw()
            comp.draw()
            ball.draw()

            player.score(str(player_score), (WIDTH//4, HEIGHT//12))
            comp.score(str(comp_score), (WIDTH-WIDTH//4, HEIGHT//12))


            pygame.display.flip()
            dt = clock.tick(60)
        
        # Display Win text
        if player_score > comp_score:
            result = "Win"
            point_sound.play()
            time.sleep(0.15)
            hit_sound.play()
        else:
            result = "Lose"
            hit_sound.play()
            point_sound.play()
            
        screen.fill(BLACK)

        font = pygame.font.SysFont('arial', TEXT_SIZE * 2)
        winner_text = font.render(f"You {result}!", True, (255, 255, 255))
        screen.blit(winner_text, (WIDTH//2 - winner_text.get_width()//2,
                                    HEIGHT//2 - winner_text.get_height()//2))
        pygame.display.flip()

        time.sleep(3)
        break

if __name__ == "__main__":
    main()
