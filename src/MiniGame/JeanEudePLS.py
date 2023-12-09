from src.Button import Button
from src.ColorPalette import *
from src.DisplayAction import DisplayAction
from src.Timer import Timer
from src.Pause import Pause

import random

class MiniGameJeanEudePLS:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen

        self._action = DisplayAction(pygame, screen, "Slap Jean-Eude!")
        self._msg = DisplayAction(pygame, screen, "Jean-Eude is KO!", "assets/sfx/excellent.ogg")

        self._hand = [None, None]

        self._timer = Timer(pygame, screen, 5)
        self._pause = Pause(pygame, screen)

        self._currentMousePos = (0, 0)
        self._prevMousePos = (0, 0)
        self._currentMouseVector = [0, 0]
        self._previousMouseVector = [0, 0]

    def loadScene(self, sceneManager):
        self._timer.reset()

        self._slapCount = 0
        self._slappCountMax = 20 + sceneManager.getDifficulty() * 5
        self._gameChanged = False

        self._jeaneude = self._pygame.image.load("assets/img/jeaneude.png")
        self._jeaneude = self._pygame.transform.scale(self._jeaneude, ((self._jeaneude.get_width() // 2) * 1.5, (self._jeaneude.get_height() // 2) * 1.5))

        self._hand[0] = self._pygame.image.load("assets/img/hands2.png")
        self._hand[0] = self._pygame.transform.rotate(self._hand[0], -10)
        self._hand[0] = self._pygame.transform.scale(self._hand[0], (self._hand[0].get_width() * 2, self._hand[0].get_height() * 2))
        self._hand[1] = self._pygame.image.load("assets/img/hands1.png")
        self._hand[1] = self._pygame.transform.rotate(self._hand[1], 20)
        self._hand[1] = self._pygame.transform.scale(self._hand[1], (self._hand[1].get_width() * 2, self._hand[1].get_height() * 2))


        self._jeaneude_pos = (self._screen.get_width() // 2 - self._jeaneude.get_width() // 2, self._screen.get_height() // 2 - self._jeaneude.get_height() // 2 - 100)

        self._isNotSlapping = True
        self._isShaking = False
        self._shakingDuration = 0
        self._shakingAmplitude = 50

    def unloadScene(self, sceneManager):
        self._jeaneude = None
        self._hand[0] = None
        self._hand[1] = None

    def run(self, sceneManager):
        self._currentMousePos = sceneManager._mouse.getPos()
        mid_screen = self._screen.get_width() // 2

        if self._currentMousePos[0] >= mid_screen and self._isNotSlapping:
            self._isNotSlapping = False
            self._slapCount += 1
            self._pygame.mixer.Sound("assets/sfx/slap.ogg").play()
        elif self._currentMousePos[0] < mid_screen and not self._isNotSlapping:
            self._isNotSlapping = True
            self._slapCount += 1
            self._pygame.mixer.Sound("assets/sfx/slap.ogg").play()
            if self._slapCount % 10 == 0:
                self._jeaneude = self._pygame.image.load("assets/img/jeaneude-frapper.png")
                self._jeaneude = self._pygame.transform.scale(self._jeaneude, ((self._jeaneude.get_width() // 2) * 1.5, (self._jeaneude.get_height() // 2) * 1.5))
                self._jeaneude = self._pygame.transform.flip(self._jeaneude, True, False)

                self._isShaking = True
                self._shakingDuration = 20

                self._pygame.mixer.Sound("assets/sfx/hurt.ogg").play()

        self._currentMouseVector[0] = self._currentMousePos[0] - self._prevMousePos[0]
        self._currentMouseVector[1] = self._currentMousePos[1] - self._prevMousePos[1]

        if self._isShaking:
            if self._shakingDuration > 0:
                shake_x = self._jeaneude_pos[0] + random.randint(-self._shakingAmplitude, self._shakingAmplitude)
                shake_y = self._jeaneude_pos[1] + random.randint(-self._shakingAmplitude, self._shakingAmplitude)
                self._screen.blit(self._jeaneude, (shake_x, shake_y))
                self._shakingDuration -= 1
            else:
                self._isShaking = False
                self._screen.blit(self._jeaneude, self._jeaneude_pos)
        else:
            self._screen.blit(self._jeaneude, self._jeaneude_pos)

        if self._currentMousePos[0] >= mid_screen:
            self._screen.blit(self._hand[0], self._currentMousePos)
        else:
            self._screen.blit(self._hand[1], self._currentMousePos)

        self._prevMousePos = self._currentMousePos
        self._previousMouseVector[0] = self._currentMouseVector[0]
        self._previousMouseVector[1] = self._currentMouseVector[1]
        self._action.display()

        if self._slapCount == self._slappCountMax:
            self._pygame.mixer.Sound("assets/sfx/cavapadutou.ogg").play()
            self._jeaneude = self._pygame.image.load("assets/img/jeaneude-triste.png")
            self._jeaneude = self._pygame.transform.scale(self._jeaneude, ((self._jeaneude.get_width() // 2) * 1.5, (self._jeaneude.get_height() // 2) * 1.5))
            self._screen.blit(self._jeaneude, self._jeaneude_pos)


        if self._slapCount >= self._slappCountMax:
            if self._msg.display() and not self._gameChanged:
                sceneManager.incrementDifficulty()
                sceneManager.incrementScore()
                sceneManager.changeScene("MiniGameMarioGalaxy")
                self._gameChanged = True
        elif self._timer.display():
            sceneManager.changeScene("LoseMenu")

        self._pause.display(sceneManager)
        sceneManager.displayScore()
