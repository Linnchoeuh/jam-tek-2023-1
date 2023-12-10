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
        self._msg = DisplayAction(pygame, screen, "You elevated enough!", "assets/music/win-doodle.ogg")

        self._pause = Pause(pygame, screen)

        self._currentMousePos = (0, 0)
        self._prevMousePos = (0, 0)

        self._timer = Timer(pygame, screen, 10)

        self._doodlerSpeed = 10
        self._gameChanged = False

        self._boeing_list = []


    def loadScene(self, sceneManager):
        self._action.reset()
        self._msg.reset()
        self._timer.reset()
        self._pause.reset()
        self._gameChanged = False

        self._doodler = self._pygame.image.load("assets/img/doodler.png")
        self._doodler = self._pygame.transform.scale(self._doodler, (self._doodler.get_width() // 6, self._doodler.get_height() // 6))
        self._doodler = self._pygame.transform.flip(self._doodler, True, False)

        self._platform = self._pygame.image.load("assets/img/platform.png")
        self._platform = self._pygame.transform.scale(self._platform, (self._platform.get_width() * 1.5, self._platform.get_height() * 1.5))

        self._platforms_pos = []

        first_platform_pos = (self._screen.get_width() // 2 - self._platform.get_width() // 2, self._screen.get_height() - self._platform.get_height() - 100)
        self._platforms_pos.append(first_platform_pos)

        lastX = first_platform_pos[0]
        for i in range(1, 10 + sceneManager.getDifficulty()):
            prev_platform_x, prev_platform_y = self._platforms_pos[i-1]

            min_x = max(prev_platform_x - 350, self._platform.get_width() // 2)
            max_x = min(prev_platform_x + 350, self._screen.get_width() - self._platform.get_width() // 2)
            # min_x = 0
            # max_x = self._screen.get_width() - self._platform.get_width()
            platform_x = random.randint(min_x, max_x)
            prev_platform_x = platform_x

            platform_y = prev_platform_y - 100
            platform_pos = (platform_x, platform_y)
            self._platforms_pos.append(platform_pos)

        self._timer = Timer(self._pygame, self._screen, 10 + sceneManager.getDifficulty() * 2)

        self._doodler_pos = (self._screen.get_width() // 6 - self._doodler.get_width() // 6, self._screen.get_height() - self._doodler.get_height() - 100)
        self._isFlipping = False

        self._isJumping = False
        self._verticalSpeed = 0
        self._gravity = 0.5
        self._ground_level = self._screen.get_height() - self._doodler.get_height() - 100
        self._jump_speed = -10

        self._action.reset()
        self._msg.reset()

    def unloadScene(self, sceneManager):
        self._doodler = None
        self._platform = None

    def run(self, sceneManager):
        self._currentMousePos = sceneManager._mouse.getPos()
        mid_screen = self._screen.get_width() // 2

        newX = self._doodler_pos[0]
        mouseOffsetX = (self._currentMousePos[0] - self._doodler.get_width() / 2)
        if self._doodler_pos[0] - mouseOffsetX > 0:
            newX -= min(self._doodlerSpeed, abs(self._doodler_pos[0] - mouseOffsetX))
        elif mouseOffsetX - self._doodler_pos[0] > 0:
            newX += min(self._doodlerSpeed, abs(self._doodler_pos[0] - mouseOffsetX))
        self._doodler_pos = (newX, self._doodler_pos[1])

        if self._currentMousePos[0] < mid_screen and self._isFlipping:
                self._doodler = self._pygame.transform.flip(self._doodler, True, False)
                self._isFlipping = False
        elif self._currentMousePos[0] > mid_screen and not self._isFlipping:
                self._doodler = self._pygame.transform.flip(self._doodler, True, False)
                self._isFlipping = True

        for i in range(len(self._platforms_pos)):
            self._screen.blit(self._platform, self._platforms_pos[i])
        self._screen.blit(self._doodler, self._doodler_pos)

        for platform_x, platform_y in self._platforms_pos:
            if self.check_collision(self._doodler_pos, (platform_x, platform_y)):
                self._pygame.mixer.Sound("assets/sfx/jump.ogg").play()
                self._isJumping = True
                self._verticalSpeed = self._jump_speed
                break

        if self._isJumping:
            self._verticalSpeed += self._gravity

            if self._verticalSpeed < 0:
                for i in range(len(self._platforms_pos)):
                    self._platforms_pos[i] = (self._platforms_pos[i][0], self._platforms_pos[i][1] - self._verticalSpeed)
            elif self._verticalSpeed > 0:
                for i in range(len(self._platforms_pos)):
                    self._platforms_pos[i] = (self._platforms_pos[i][0], self._platforms_pos[i][1] - self._verticalSpeed)

        if not self._gameChanged and \
        self._platforms_pos[len(self._platforms_pos) - 1][1] > self._screen.get_height() - self._platform.get_height():
            sceneManager.nextGame()
            self._msg.display()
            self._gameChanged = True
        elif self._platforms_pos[0][1] < 0:
            sceneManager.changeScene("LoseMenu")

        if self._timer.display():
            sceneManager.changeScene("LoseMenu")
        self._prevMousePos = self._currentMousePos
        self._action.display()

        self._pause.display(sceneManager)
        sceneManager.displayScore()

    def check_collision(self, doodler_pos, platform_pos):
        doodler_x, doodler_y = doodler_pos
        platform_x, platform_y = platform_pos

        if doodler_x + self._doodler.get_width() >= platform_x and doodler_x <= platform_x + self._platform.get_width():
            if doodler_y + self._doodler.get_height() + 5 >= platform_y and doodler_y <= platform_y + self._platform.get_height():
                return True
        return False
