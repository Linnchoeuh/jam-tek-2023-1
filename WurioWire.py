import pygame

from src.Scenes.SceneManager import SceneManager
from src.Animation import Animation

# Initialize pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Game")

# Create a clock object
clock = pygame.time.Clock()

spriteSheet = pygame.image.load("assets/sprite/player3Down.png")
animationGroup = pygame.sprite.Group()
animationGroup.add(Animation(spriteSheet, 4, 1))
SceneManager = SceneManager(pygame, screen)
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
    screen.fill((0, 0, 0))

    SceneManager.displayScene()
    animationGroup.update()
    animationGroup.draw(screen)
    pygame.display.flip()

    # Limit the frame rate to 60 FPS
    clock.tick(60)

# Quit the game
pygame.quit()
