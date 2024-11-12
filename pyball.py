import pygame
import sys

WIDTH = 640
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH,HEIGHT))

BLACK = (0,0,0)


class Player_Block:

    def __init__(self, pos=(0,0)):
        self.pos = pygame.Vector2(pos)
        self.width = 25
        self.height = 100
        self.color = (255,255,255)
        self.speed = 3.0

        # Rect Properties
        self.block_controller = pygame.Rect(pos[0], pos[1], self.width, self.height)
        # Display Rect
        self.block = pygame.draw.rect(screen, self.color, self.block_controller)

    def move(self, dir):
        self.pos = self.pos + dir * self.speed

        self.block_controller = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)

    def draw(self):
        self.block = pygame.draw.rect(screen, self.color, self.block_controller)
        

def main():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0

    # Window Title
    pygame.display.set_caption("PyBall: Retro Edition")

    #Create Player
    player = Player_Block(pos=(WIDTH//16,HEIGHT//2))

    # Game loop to keep the window open
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.pos[1] > 2:
            player.move(pygame.Vector2(0, -1.5))
        if keys[pygame.K_DOWN] and player.pos[1] < HEIGHT-player.height-2:
            player.move(pygame.Vector2(0, 1.5))

        screen.fill(BLACK)
        player.draw()
        # Update display
        pygame.display.flip()
        dt = clock.tick(30)

if __name__ == "__main__":
    main()