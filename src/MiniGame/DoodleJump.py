from src.Button import Button
from src.ColorPalette import *
from src.DisplayAction import DisplayAction
from src.Timer import Timer
from src.Pause import Pause

import random

class MiniGameDoodleJump:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen

        self._action = DisplayAction(pygame, screen, "Jump on the platforms!")
        self._msg = DisplayAction(pygame, screen, "You won!", "assets/sfx/excellent.ogg")

        self._timer = Timer(pygame, screen, 5)
        self._pause = Pause(pygame, screen)

        self._currentMousePos = (0, 0)
        self._prevMousePos = (0, 0)

    def loadScene(self, sceneManager):
        self._timer.reset()

        self._gameChanged = False

        self._doodler = self._pygame.image.load("assets/img/doodler.png")
        self._doodler = self._pygame.transform.scale(self._doodler, (self._doodler.get_width() // 6, self._doodler.get_height() // 6))
        self._doodler = self._pygame.transform.flip(self._doodler, True, False)

        self._platform = self._pygame.image.load("assets/img/platform.png")
        self._platform = self._pygame.transform.scale(self._platform, (self._platform.get_width() * 1.5, self._platform.get_height() * 1.5))

        self._platforms_pos = []

        for i in range(10 + sceneManager.getDifficulty() * 5):
            x = random.randint(0, self._screen.get_width() - self._platform.get_width())
            y = random.randint(0, self._screen.get_height() - self._platform.get_height())
            self._platforms_pos.append((x, y))

        self._doodler_pos = (self._screen.get_width() // 6 - self._doodler.get_width() // 6, self._screen.get_height() - self._doodler.get_height() - 100)

        self._gravity = 1
        self._jump_speed = -10
        self._vertical_speed = 0
        self._isJumping = False
        self._ground_level = self._screen.get_height() - 100

        self._jumpCount = 0
        self._jumpCountMax = 50 + sceneManager.getDifficulty() * 5
        self._haveJumped = False

        self._isFlipping = False

    def unloadScene(self, sceneManager):
        self._doodler = None
        self._platform = None

    def run(self, sceneManager):
        self._currentMousePos = sceneManager._mouse.getPos()
        mid_screen = self._screen.get_width() // 2

        if self._currentMousePos[0] < mid_screen:
            self._doodler_pos = (self._doodler_pos[0] - 5, self._doodler_pos[1])
            if self._isFlipping:
                self._doodler = self._pygame.transform.flip(self._doodler, True, False)
                self._isFlipping = False
        else:
            self._doodler_pos = (self._doodler_pos[0] + 5, self._doodler_pos[1])
            if not self._isFlipping:
                self._doodler = self._pygame.transform.flip(self._doodler, True, False)
                self._isFlipping = True

        if not self._isJumping:
            self._vertical_speed += self._gravity
        else:
            self._vertical_speed = self._jump_speed
            self._isJumping = False

        for i in range(len(self._platforms_pos)):
            self._platforms_pos[i] = (self._platforms_pos[i][0], self._platforms_pos[i][1] + self._vertical_speed)

        for platform_x, platform_y in self._platforms_pos:
            if self.check_collision(self._doodler_pos, (platform_x, platform_y)):
                self._isJumping = True
                if not self._haveJumped:
                    self._haveJumped = True
                    self._jumpCount += 1
                break

        self._haveJumped = False

        self._screen.blit(self._doodler, self._doodler_pos)

        for i in range(len(self._platforms_pos)):
            self._screen.blit(self._platform, self._platforms_pos[i])

        self._prevMousePos = self._currentMousePos
        self._action.display()

        if self._jumpCount >= self._jumpCountMax:
            if self._msg.display() and not self._gameChanged:
                sceneManager.incrementDifficulty()
                sceneManager.incrementScore()
                sceneManager.changeScene("MiniGameJeanEudePLS")
                self._gameChanged = True
        elif self._timer.display():
            sceneManager.changeScene("LoseMenu")

        self._pause.display(sceneManager)
        sceneManager.displayScore()

    def check_collision(self, doodler_pos, platform_pos):
        doodler_x, doodler_y = doodler_pos
        platform_x, platform_y = platform_pos

        if doodler_x + self._doodler.get_width() >= platform_x and doodler_x <= platform_x + self._platform.get_width():
            if doodler_y + self._doodler.get_height() >= platform_y and doodler_y <= platform_y + self._platform.get_height():
                return True
        return False
