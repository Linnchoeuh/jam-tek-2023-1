from src.Button import Button
from src.ColorPalette import *
from src.DisplayAction import DisplayAction

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
        # self._action = DisplayAction(pygame, screen, "Wurio Wire")

    def loadScene(self, sceneManager):
        # self._action.reset()
        pass

    def unloadScene(self, sceneManager):
        pass

    def run(self, sceneManager):
        # Draw a simple square
        self._screen.blit(self.text_surface, (10, 10))
        self._playButton.display()
        self._quitButton.display()

        # self._action.display()

        if (self._quitButton.isClicked(sceneManager._mouse)):
            self._pygame.event.post(self._pygame.event.Event(self._pygame.QUIT))
        if (self._playButton.isClicked(sceneManager._mouse)):
            sceneManager.setDifficulty(0)
            sceneManager.resetGameList()
            sceneManager.nextGame()
            sceneManager.setScore(0)
            # sceneManager.changeScene("MiniGameWiiPlayTanks")
