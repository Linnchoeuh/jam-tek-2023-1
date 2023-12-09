import random

from src.Button import Button
from src.ColorPalette import *
from src.DisplayAction import DisplayAction
from src.Timer import Timer
from src.Pause import Pause


class MiniGameMarioGalaxy:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen
        self._stars = []
        for i in range(0, 100):
            self._stars.append((random.randint(0, screen.get_width()), random.randint(0, screen.get_height())))
        self._action = DisplayAction(pygame, screen, "Shake your mouse!")
        self._msg = DisplayAction(pygame, screen, "Nice!")
        self._timer = Timer(pygame, screen, 5)
        self._pause = Pause(pygame, screen)

        self._currentMousePos = (0, 0)
        self._prevMousePos = (0, 0)
        self._currentMouseVector = [0, 0]
        self._previousMouseVector = [0, 0]
        self._shakeCount = 0
        self._shakeCountMax = 10
        self._gameChanged = False

    def loadScene(self, sceneManager):
        self._action.reset()
        self._msg.reset()
        self._timer.reset()
        self._pause.reset()
        self._shakeCount = 0
        self._shakeCountMax = 20 + sceneManager.getDifficulty() * 5
        self._gameChanged = False
        pass

    def unloadScene(self, sceneManager):
        pass

    def run(self, sceneManager):
        self._currentMousePos = sceneManager._mouse.getPos()

        self._currentMouseVector[0] = self._currentMousePos[0] - self._prevMousePos[0]
        self._currentMouseVector[1] = self._currentMousePos[1] - self._prevMousePos[1]

        if self._currentMouseVector[0] * self._previousMouseVector[0] < 0 or \
        self._currentMouseVector[1] * self._previousMouseVector[1] < 0 or \
        ((self._currentMouseVector[0] != 0 and self._previousMouseVector[1] == 0) and \
        (self._currentMouseVector[1] != 0 and self._previousMouseVector[0] == 0)):
            self._shakeCount += 1
            print(self._shakeCount)

        self._prevMousePos = self._currentMousePos
        self._previousMouseVector[0] = self._currentMouseVector[0]
        self._previousMouseVector[1] = self._currentMouseVector[1]

        for star in self._stars:
            self._pygame.draw.circle(self._screen, GBACOLOR3, star, 2)

        self._action.display()
        if self._shakeCount >= self._shakeCountMax:
            if self._msg.display() and not self._gameChanged:
                sceneManager.incrementDifficulty()
                sceneManager.incrementScore()
                sceneManager.changeScene("MiniGameMarioGalaxy")
                self._gameChanged = True
        elif self._timer.display():
            sceneManager.changeScene("LoseMenu")
        self._pause.display(sceneManager)
        sceneManager.displayScore()
