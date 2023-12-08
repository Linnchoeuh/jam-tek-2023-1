from src.Button import Button
from src.ColorPalette import *

class MainMenu:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen
        buttonWidth = 300
        centered_posX = screen.get_width() / 2 - buttonWidth / 2
        self.font = pygame.font.Font(None, 100)
        self.text_surface = self.font.render("Wurio Wire", True, GBACOLOR3)

        self._playButton = Button(pygame, screen, centered_posX, 200, buttonWidth, 100, "Play")
        self._quitButton = Button(pygame, screen, centered_posX, 400, buttonWidth, 100, "Quit")

    def loadScene(self, sceneManager):
        pass

    def unloadScene(self, sceneManager):
        pass

    def run(self, sceneManager):
        # Draw a simple square
        text_rect = self.text_surface.get_rect()
        self._screen.blit(self.text_surface, text_rect)
        self._playButton.display()
        self._quitButton.display()

        if (self._quitButton.isClicked(sceneManager.getEvents())):
            self._pygame.event.post(self._pygame.event.Event(self._pygame.QUIT))
        if (self._playButton.isClicked(sceneManager.getEvents())):
            sceneManager.changeScene("TestMenu")
