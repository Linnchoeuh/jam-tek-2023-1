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
        self._msg = DisplayAction(pygame, screen, "Nice!", "assets/sfx/excellent.ogg")
        self._timer = Timer(pygame, screen, 5)
        self._pause = Pause(pygame, screen)

        self._shake1 = None
        self._shake2 = None
        self._load_and_launch = None

        self._star = None
        self._rotation = random.randint(0, 360)
        self._rotationSpeed = 0
        self._maxRotation = 20
        self._rotationDeceleration = 0.3
        self._planet = None
        self._mario = None
        self._offsetY = 0
        self._delay = 0


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

        self._shake1 = self._pygame.mixer.Sound("assets/sfx/star_shake1.ogg")
        self._shake2 = self._pygame.mixer.Sound("assets/sfx/star_shake2.ogg")
        self._load_and_launch = self._pygame.mixer.Sound("assets/sfx/star_load_and_launch.ogg")

        self._star = self._pygame.image.load("assets/img/star_launcher.png")
        self._rotationSpeed = 0
        self._star = self._pygame.transform.scale(self._star, (300, 300))
        self._planet = self._pygame.image.load("assets/img/planet.png")
        self._mario = self._pygame.image.load("assets/img/mario.png")
        self._mario = self._pygame.transform.scale(self._mario, (130, 200))
        self._offsetY = 0
        self._delay = 40

    def unloadScene(self, sceneManager):
        self._shake1 = None
        self._shake2 = None
        self._load_and_launch = None

        self._star = None
        self._planet = None
        self._mario = None

    def run(self, sceneManager):
        self._currentMousePos = sceneManager._mouse.getPos()

        self._currentMouseVector[0] = self._currentMousePos[0] - self._prevMousePos[0]
        self._currentMouseVector[1] = self._currentMousePos[1] - self._prevMousePos[1]

        if self._currentMouseVector[0] * self._previousMouseVector[0] < 0 or \
        self._currentMouseVector[1] * self._previousMouseVector[1] < 0 or \
        ((self._currentMouseVector[0] != 0 and self._previousMouseVector[1] == 0) and \
        (self._currentMouseVector[1] != 0 and self._previousMouseVector[0] == 0)):
            if self._shakeCountMax - self._shakeCount > 10:
                self._shake2.play()
            elif self._shakeCount < self._shakeCountMax:
                self._shake1.play()
            self._shakeCount += 1
            self._rotationSpeed = self._maxRotation
            # print(self._shakeCount)

        if self._shakeCount == self._shakeCountMax:
            self._load_and_launch.play()
            self._shakeCount += 1

        self._prevMousePos = self._currentMousePos
        self._previousMouseVector[0] = self._currentMouseVector[0]
        self._previousMouseVector[1] = self._currentMouseVector[1]

        # bg stars
        for star in self._stars:
            self._pygame.draw.circle(self._screen, GBACOLOR3, (star[0], (star[1] + self._offsetY) % self._screen.get_height()), 2)

        # planet
        self._screen.blit(self._planet, (self._screen.get_width() / 2 - 300, 200 + self._offsetY))

        # star launcher
        tmpStart = self._pygame.transform.rotate(self._star, self._rotation)

        self._screen.blit(tmpStart, (self._screen.get_width() / 2 - 180, 200 + self._offsetY))

        self._rotation += self._rotationSpeed
        if self._rotationSpeed > 0:
            self._rotationSpeed -= self._rotationDeceleration

        # mario
        self._screen.blit(self._mario, ((self._screen.get_width() / 2 - 50) + self._previousMouseVector[0], 300 + self._previousMouseVector[1]))

        self._action.display()
        if self._shakeCount >= self._shakeCountMax:
            self._rotationSpeed = 60
            if self._msg.display() and not self._gameChanged:
                sceneManager.nextGame()
                self._gameChanged = True
            if self._delay > 0:
                self._delay -= 1
            else:
                self._offsetY += 30
        elif self._timer.display():
            sceneManager.changeScene("LoseMenu")
        self._pause.display(sceneManager)
        sceneManager.displayScore()
