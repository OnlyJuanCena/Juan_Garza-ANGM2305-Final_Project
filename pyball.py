import pygame

WIDTH = 640
HEIGHT = 480

def main():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Create Window
    screen = pygame.display.set_mode((WIDTH,HEIGHT))

    # Window Title
    pygame.display.set_caption("PyBall: Retro Edition")

    # Game loop to keep the window open
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(pygame.Vector2(0, -1.5))
        if keys[pygame.K_DOWN]:
            player.move(pygame.Vector2(0, 1.5))
        if keys[pygame.K_LEFT]:
            player.move(pygame.Vector2(-1.5, 0))
        if keys[pygame.K_RIGHT]:
            player.move(pygame.Vector2(1.5, 0))