from src.Button import Button

class TestMenu:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen
        buttonWidth = 300
        centered_posX = screen.get_width() / 2 - buttonWidth / 2

        self._backButton = Button(pygame, screen, centered_posX, 200, buttonWidth, 100, "Back")
    def loadScene(self, sceneManager):
        pass

    def unloadScene(self, sceneManager):
        pass

    def run(self, sceneManager):
        self._backButton.display()

        if (self._backButton.isClicked(sceneManager._mouse)):
            sceneManager.changeScene("MainMenu")
