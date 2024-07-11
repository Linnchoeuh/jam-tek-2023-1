import random

from src.Button import Button
from src.ColorPalette import *
from src.DisplayAction import DisplayAction
from src.Timer import Timer
from src.Pause import Pause

class MiniGameFarminions:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen
        self._action = DisplayAction(pygame, screen, "Farm minions!")
        self._msg = DisplayAction(pygame, screen, "Nice!")
        self._imgs = [pygame.image.load("assets/sprite/minionMelee.png"), pygame.image.load("assets/sprite/minionRange.png"), pygame.image.load("assets/sprite/minionBackground.png")]
        self._coinSound = pygame.mixer.Sound("assets/sfx/Coins.ogg")
        self._timer = Timer(pygame, screen, 6)
        self._pause = Pause(pygame, screen)
        self._currentMousePos = (0, 0)
        self._targetNbrFarm = 8
        self._nbrFarm = 0
        self._gameChanged = False
        self._gameOver = False
        self._mouseClick = False
        self._spawned = 0

    def loadScene(self, sceneManager):
        self._action.reset()
        self._msg.reset()
        self._timer.reset()
        self._pause.reset()
        self._nbrFarm = 0
        self._targetNbrFarm = 5 + sceneManager.getDifficulty()
        if self._targetNbrFarm > 10:
            self._targetNbrFarm = 10
        self._farmOnScreen = []
        self._gameChanged = False
        self._gameOver = False
        self._spawned = 0
        pass

    def unloadScene(self, sceneManager):
        self._nbrFarm = 0
        self._farmOnScreen.clear()
        self._gameOver = False
        pass

    def run(self, sceneManager):
        self._currentMousePos = sceneManager._mouse.getPos()


        self._screen.blit(self._imgs[2], self._imgs[2].get_rect())
        if self._spawned < self._targetNbrFarm  and len(self._farmOnScreen) < 2:
            self._spawned += 1
            imgPos = random.randint(0, 1)
            self._farmOnScreen.append(Minion(self._pygame, self._screen, self._pygame.transform.scale(self._imgs[imgPos], (self._imgs[imgPos].get_width() / 4, self._imgs[imgPos].get_height() / 4))))
        for i in range(len(self._farmOnScreen)):
            self._farmOnScreen[i].display()
        for i in range(len(self._farmOnScreen)):
            hit, self._mouseClick = mouseClicked(self._currentMousePos, self._farmOnScreen[i], self._mouseClick)
            if hit:
                self._farmOnScreen.pop(i)
                self._nbrFarm += 1
                self._coinSound.play()
                break

        self._action.display()
        if self._nbrFarm >= self._targetNbrFarm:
            self._farmOnScreen.clear()
            if self._msg.display() and not self._gameChanged:
                sceneManager.nextGame()
                self._gameChanged = True
        elif self._gameOver:
                sceneManager.changeScene("LoseMenu")
        if self._gameOver == False:
            self._gameOver = self._timer.display()
        self._pause.display(sceneManager)
        sceneManager.displayScore()

class Minion:
    def __init__(self, pygame, screen, img):
        self._pygame = pygame
        self._screen = screen
        self._img = img
        self._img = pygame.transform.scale(self._img, (self._img.get_width(), self._img.get_height()))
        self._rect = self._img.get_rect()
        self._spawnX = int(self._rect.width * 1.5)
        self._spawnY = int(self._rect.height * 1.5)
        self._rect.x = random.randint(1, int(screen.get_width() / 50) - 3) * 50
        self._rect.y = random.randint(1, int(screen.get_height() / 50) - 3) * 50

    def display(self):
        self._screen.blit(self._img, self._rect)

def mouseCollision(mousePos, entity):
    return entity._rect.collidepoint(mousePos)

def mouseClicked(mousePos, entity, mouseClick):
    if (mouseClick == False and entity._pygame.mouse.get_pressed()[0]):
        mouseClick = True
    if (mouseClick == True and not entity._pygame.mouse.get_pressed()[0] and entity._rect.collidepoint(mousePos)):
        mouseClick = False
        return True, mouseClick
    return False, mouseClick
