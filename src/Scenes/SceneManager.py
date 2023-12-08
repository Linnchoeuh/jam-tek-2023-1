from src.ColorPalette import *
from src.Scenes.MainMenu import MainMenu
from src.Scenes.TestMenu import TestMenu

class SceneManager:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen

        self._sceneList: dict = {
            "MainMenu": MainMenu(pygame, screen),
            "TestMenu": TestMenu(pygame, screen),
        }
        self._currentScene = "None"
        self._nextScene = "None"
        self.switchScene("MainMenu")
        self._events = pygame.event.get()
        self._transitionStart = -1;
        self._transitionEnd = -1;

    def sceneNameExist(self, sceneName):
        return sceneName in self._sceneList

    def getScene(self, sceneName: str):
        return self._sceneList[sceneName]

    def changeScene(self, sceneName: str):
        self._nextScene = sceneName

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

        if self._nextScene != self._currentScene or self._transitionStart != -1 or self._transitionEnd != -1:
            if self._nextScene != self._currentScene and self._transitionStart < 0:
                self._transitionStart = 0
            elif self._transitionStart < 1:
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
