import sys
import os
import pygame
from vinepilot.config import Project

WIDTH, HEIGHT = 600, 800
img_path = os.path.abspath("./vinepilot/data/vineyards/vineyard_000/vineyard_1.svg")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virtual Vineyard")
image = pygame.image.load(img_path)
rect = image.get_rect()

# Main game loop
def game():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill((255, 255, 255))

        # Blit the image onto the screen
        screen.blit(image, rect)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        pygame.time.Clock().tick(60)

