from src.ColorPalette import *
from src.DisplayAction import DisplayAction
from src.Button import Button

import time

class Pause:
    def __init__(self, pygame, screen, duration = 5):
        self._pygame = pygame
        self._screen = screen
        buttonWidth = 300
        centered_posX = screen.get_width() / 2 - buttonWidth / 2
        self._show = False
        self._action = DisplayAction(pygame, screen, "Pause")
        self._action.setYPos(70)
        self._playButton = Button(pygame, screen, centered_posX, 200, buttonWidth, 100, "Resume")
        self._quitButton = Button(pygame, screen, centered_posX, 400, buttonWidth, 100, "Main Menu")

        self.reset()

    def reset(self):
        self._show = False
        self._action.reset()


    def display(self, sceneManager) -> bool:
        events = sceneManager.getEvents()
        for event in events:
            if event.type == self._pygame.KEYDOWN and event.key == self._pygame.K_ESCAPE:
                self._show = not self._show
                break
        if self._show:
            self._playButton.display()
            self._quitButton.display()
            self._action.display()
            if (self._quitButton.isClicked(sceneManager._mouse)):
                sceneManager.changeScene("MainMenu")
            if (self._playButton.isClicked(sceneManager._mouse)):
                self._show = False
        else:
            self._action.reset()
