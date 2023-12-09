from src.Button import Button
from src.ColorPalette import *
from src.DisplayAction import DisplayAction

class LoseMenu:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen
        buttonWidth = 300
        centered_posX = screen.get_width() / 2 - buttonWidth / 2
        self.font = pygame.font.Font(None, 100)
        self.text_surface = self.font.render("You lose!", True, GBACOLOR3)
        self.text_surface2 = self.font.render("Score: 0", True, GBACOLOR3)

        self._retryButton = Button(pygame, screen, centered_posX, 225, buttonWidth, 100, "Retry")
        self._playButton = Button(pygame, screen, centered_posX, 350, buttonWidth, 100, "Main Menu")
        self._quitButton = Button(pygame, screen, centered_posX, 475, buttonWidth, 100, "Quit")
        # self._action = DisplayAction(pygame, screen, "Wurio Wire")

    def loadScene(self, sceneManager):
        self.text_surface2 = self.font.render("Score: " + str(sceneManager.getScore()), True, GBACOLOR3)
        pass

    def unloadScene(self, sceneManager):
        pass

    def run(self, sceneManager):
        # Draw a simple square
        self._screen.blit(self.text_surface, (10, 10))
        self._screen.blit(self.text_surface2, (170, 110))
        self._retryButton.display()
        self._playButton.display()
        self._quitButton.display()

        if (self._quitButton.isClicked(sceneManager._mouse)):
            self._pygame.event.post(self._pygame.event.Event(self._pygame.QUIT))
        if (self._playButton.isClicked(sceneManager._mouse)):
            sceneManager.changeScene("MainMenu")
        if (self._retryButton.isClicked(sceneManager._mouse)):
            sceneManager.setDifficulty(0)
            sceneManager.resetGameList()
            sceneManager.nextGame()
            sceneManager.setScore(0)
