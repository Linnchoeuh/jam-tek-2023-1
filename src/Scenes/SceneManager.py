from src.Scenes.MainMenu import MainMenu
from src.Scenes.TestMenu import TestMenu

class SceneManager:
    def __init__(self, pygame, screen):
        self._sceneList: dict = {
            "MainMenu": MainMenu(pygame, screen),
            "TestMenu": TestMenu(pygame, screen),
        }
        self._currentScene = "None"
        self.changeScene("MainMenu")
        self._pygame = pygame
        self._screen = screen
        self._events = pygame.event.get()

    def sceneNameExist(self, sceneName):
        return sceneName in self._sceneList

    def getScene(self, sceneName: str):
        return self._sceneList[sceneName]

    def changeScene(self, sceneName: str):
        if self._currentScene != "None":
            self._sceneList[self._currentScene].unloadScene(self)
        self._currentScene = sceneName
        self._sceneList[self._currentScene].loadScene(self)

    def updatePygameEvents(self):
        self._events = self._pygame.event.get()
        return self.getEvents()

    def displayScene(self):
        self._sceneList[self._currentScene].run(self)

    def getPygame(self):
        return self._pygame

    def getScreen(self):
        return self._screen

    def getEvents(self):
        return self._events
