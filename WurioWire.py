import pygame

from src.Scenes.SceneManager import SceneManager
from src.Animation import Animation
from src.ColorPalette import *
from src.WindowConfig import *


# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREENW, SCREENH), pygame.RESIZABLE)
screenCpy = screen.copy()
pygame.display.set_caption("Wurio Wire")

# Create a clock object
clock = pygame.time.Clock()

spriteSheet = pygame.image.load("assets/sprite/player3Down.png")
animationGroup = pygame.sprite.Group()
animationGroup.add(Animation(spriteSheet, 4, 1))
SceneManager = SceneManager(pygame, screenCpy)

joffrey_left = pygame.image.load("assets/img/joffrey_left.png")
joffrey_right = pygame.image.load("assets/img/joffrey_right.png")
joffrey_width = joffrey_left.get_width()
joffrey_height = joffrey_left.get_height()
joffrey_ratio = joffrey_width / joffrey_height
screenOffset = 0


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
    animationGroup.update()
    animationGroup.draw(screen)

    screenOffset = (screen.get_size()[0] - screen.get_size()[1] * SCREENRATIO) / 2
    screenOffsetAdjusted = screenOffset
    if (screenOffsetAdjusted < 0):
        screenOffsetAdjusted = 0
    tmp = pygame.transform.scale(joffrey_left, (screenOffsetAdjusted, screen.get_size()[1]))
    screen.blit(tmp, (0, 0))
    tmp = pygame.transform.scale(joffrey_right, (screenOffsetAdjusted, screen.get_size()[1]))
    screen.blit(tmp, (screenOffset + screen.get_size()[1] * SCREENRATIO, 0))
    screen.blit(pygame.transform.scale(screenCpy, (screen.get_size()[1] * SCREENRATIO, screen.get_size()[1])), (screenOffset, 0))
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

# Quit the game
pygame.quit()
