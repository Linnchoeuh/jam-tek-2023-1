import random

from src.ColorPalette import *
from src.Mouse import Mouse
from src.Scenes.MainMenu import MainMenu
from src.Scenes.LoseMenu import LoseMenu

from src.MiniGame.MarioGalaxy import MiniGameMarioGalaxy
from src.MiniGame.JeanEudePLS import MiniGameJeanEudePLS
from src.MiniGame.DodgeDinner import MiniGameDodgeDinner
from src.MiniGame.MonsterHunter import MiniGameMonsterHunter
from src.MiniGame.DoodleJump import MiniGameDoodleJump
from src.MiniGame.WiiPlayTanks import MiniGameWiiPlayTanks

class SceneManager:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen

        self._mouse = Mouse(pygame)

        self._sceneList: dict = {
            "MainMenu": MainMenu(pygame, screen),
            "LoseMenu": LoseMenu(pygame, screen),
            "MiniGameMarioGalaxy": MiniGameMarioGalaxy(pygame, screen),
            "MiniGameJeanEudePLS": MiniGameJeanEudePLS(pygame, screen),
            "MiniGameDodgeDinner": MiniGameDodgeDinner(pygame, screen),
            "MiniGameMonsterHunter": MiniGameMonsterHunter(pygame, screen),
            "MiniGameDoodleJump": MiniGameDoodleJump(pygame, screen),
            "MiniGameWiiPlayTanks": MiniGameWiiPlayTanks(pygame, screen),
        }

        self._gameList = [
            "MiniGameMarioGalaxy",
            "MiniGameJeanEudePLS",
            "MiniGameDodgeDinner",
            "MiniGameMonsterHunter",
            "MiniGameDoodleJump",
            "MiniGameWiiPlayTanks",
        ]
        self._gameToDoList = self._gameList.copy()

        self._music = self._pygame.mixer.Sound("assets/music/wario_ware_smash_theme.ogg")
        self._music.play(-1)
        self._currentScene = "None"
        self._nextScene = "None"
        self.switchScene("MainMenu")
        self._events = pygame.event.get()
        self._transitionStart = -1
        self._transitionEnd = -1

        self._font = pygame.font.Font(None, 50)
        self._difficulty = 0
        self._score = 0

    def sceneNameExist(self, sceneName):
        return sceneName in self._sceneList

    def getScene(self, sceneName: str):
        return self._sceneList[sceneName]

    def changeScene(self, sceneName: str):
        if self._transitionStart == -1 and self._transitionEnd == -1:
            self._nextScene = sceneName
            self._transitionStart = 0

    def switchScene(self, sceneName: str):
        if self._currentScene != "None":
            self._sceneList[self._currentScene].unloadScene(self)
        self._currentScene = sceneName
        self._nextScene = sceneName
        self._sceneList[self._currentScene].loadScene(self)


    def updatePygameEvents(self):
        self._events = self._pygame.event.get()
        return self.getEvents()

    def displayScene(self):
        self._mouse.update()
        self._sceneList[self._currentScene].run(self)
        self.displayTransition()


    def getPygame(self):
        return self._pygame

    def getScreen(self):
        return self._screen

    def getEvents(self):
        return self._events

    def displayTransition(self):
        part = 0
        screenWidth = self._screen.get_width()
        leftSquare = self._pygame.Rect(0, 0, 0, 0)
        rightSquare = self._pygame.Rect(0, 0, 0, 0)
        transitionSpeed = 1/12
        transitionColor = GBACOLOR1

        if self._transitionStart != -1 or self._transitionEnd != -1:
            if self._transitionStart < 1:
                self._transitionStart += transitionSpeed
                part = (screenWidth / 2) * self._transitionStart * 1.1
                leftSquare = self._pygame.Rect(0, 0, part, self._screen.get_height())
                rightSquare = self._pygame.Rect(screenWidth - part, 0, screenWidth, self._screen.get_height())
            elif self._transitionStart >= 1 and self._transitionEnd < 0:
                self._screen.fill(transitionColor)
                self._pygame.display.flip()
                self.switchScene(self._nextScene)
                self._transitionEnd = 0
            elif self._transitionEnd < 1:
                self._transitionEnd += transitionSpeed
                screenWidth = self._screen.get_width()
                part = (screenWidth / 2) * (1 - self._transitionEnd) * 1.1
                leftSquare = self._pygame.Rect(0, 0, part, self._screen.get_height())
                rightSquare = self._pygame.Rect(screenWidth - part, 0, screenWidth, self._screen.get_height())
            else:
                self._transitionStart = -1
                self._transitionEnd = -1
            self._pygame.draw.rect(self._screen, transitionColor, leftSquare)
            self._pygame.draw.rect(self._screen, transitionColor, rightSquare)

    def getDifficulty(self):
        return self._difficulty

    def incrementDifficulty(self):
        self._difficulty += 1

    def setDifficulty(self, difficulty):
        self._difficulty = difficulty

    def getScore(self):
        return self._score

    def incrementScore(self):
        self._score += 1

    def setScore(self, score):
        self._score = score

    def displayScore(self):
        text_surface = self._font.render("Score: " + str(self._score), True, GBACOLOR3)
        self._screen.blit(text_surface, (10, 10))

    def updateMouse(self, screen):
        self._mouse.scalePosition(screen.get_width(), screen.get_height())

    def resetGameList(self):
        self._gameToDoList = self._gameList.copy()

    def nextGame(self):
        if len(self._gameToDoList) == 0:
            self.incrementDifficulty()
            self.resetGameList()
        # print("TO DO: ", self._gameToDoList)
        pickedGame = random.randint(0, len(self._gameToDoList) - 1)
        self.changeScene(self._gameToDoList[pickedGame])
        self._gameToDoList.pop(pickedGame)
        self.incrementScore()
