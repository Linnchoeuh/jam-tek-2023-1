import pygame

from src.Scenes.SceneManager import SceneManager
from src.ColorPalette import *
from src.WindowConfig import *


# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREENW, SCREENH), pygame.RESIZABLE)
screenCpy = screen.copy()
pygame.display.set_caption("My Game")

# Create a clock object
clock = pygame.time.Clock()


SceneManager = SceneManager(pygame, screenCpy)
# Game loop
running = True
while running:
    # Handle events
    events = SceneManager.updatePygameEvents()
    for event in events:
        if event.type == pygame.QUIT:
            running = False


    # Update game logic

    # Render the screen
    screenCpy.fill(GBACOLOR0)

    SceneManager.updateMouse(screen)
    SceneManager.displayScene()

    screen.blit(pygame.transform.scale(screenCpy, (screen.get_size()[1] * SCREENRATIO, screen.get_size()[1])), ((screen.get_size()[0] - screen.get_size()[1] * SCREENRATIO) / 2, 0))
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

# Quit the game
pygame.quit()
