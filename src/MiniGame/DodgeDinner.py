import random

from src.Button import Button
from src.ColorPalette import *
from src.DisplayAction import DisplayAction
from src.Timer import Timer
from src.Pause import Pause


class MiniGameDodgeDinner:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen
        self._stars = []
        for i in range(0, 100):
            self._stars.append((random.randint(0, screen.get_width()), random.randint(0, screen.get_height())))
        self._action = DisplayAction(pygame, screen, "Dodge utensils!")
        self._msg = DisplayAction(pygame, screen, "Nice!")
        self._timer = Timer(pygame, screen, 5)
        self._pause = Pause(pygame, screen)
        self._utensils = []
        self._currentMousePos = (0, 0)
        self.utensilsSpeed = 10
        self._warmup = 1.0
        self._gameChanged = False

    def loadScene(self, sceneManager):
        self._action.reset()
        self._msg.reset()
        self._timer.reset()
        self._pause.reset()
        self._warmup = 1.0

        self.utensilsSpeed = 14 + sceneManager.getDifficulty() * 2
        if self.utensilsSpeed > 20:
            self.utensilsSpeed = 20
        self._gameChanged = False
        pass

    def unloadScene(self, sceneManager):
        pass

    def run(self, sceneManager):
        self._currentMousePos = sceneManager._mouse.getPos()

        for star in self._stars:
            self._pygame.draw.circle(self._screen, GBACOLOR3, star, 2)

        for utensil in self._utensils:
            utensil.move(self.utensilsSpeed)
            utensil.display()
            if utensil._rect.x > self._screen.get_width() + utensil._rect.width or utensil._rect.x < 0 - utensil._rect.width - 10:
                self._utensils.remove(utensil)

        if self._warmup < 0:
            if len(self._utensils) < 3 + sceneManager.getDifficulty():
                if random.randint(0, 1):
                    self._utensils.append(Fork(self._pygame, self._screen, random.randint(0, self._screen.get_height())))
                else:
                    self._utensils.append(Knife(self._pygame, self._screen, random.randint(0, int(self._currentMousePos[1]))))
        else:
            self._warmup -= 0.01

        self._action.display()
        if self._timer.display():
            self._utensils.clear()
            if self._msg.display() and not self._gameChanged:
                sceneManager.nextGame()
                self._gameChanged = True
        for utensil in self._utensils:
            if mouseCollision(self._currentMousePos, utensil):
                sceneManager.changeScene("LoseMenu")
        self._pause.display(sceneManager)
        sceneManager.displayScore()

class Fork:
    def __init__(self, pygame, screen, y = 0):
        self._pygame = pygame
        self._screen = screen
        self._img = pygame.image.load("assets/sprite/fork.png")
        self._img = pygame.transform.scale(self._img, (self._img.get_width() * 3, self._img.get_height() * 3))
        self._rect = self._img.get_rect()
        self._rect.x = 0 - self._rect.width - 10
        self._rect.y = y

    def display(self):
        self._screen.blit(self._img, self._rect)

    def move(self, speed):
        self._rect.x += speed

class Knife:
    def __init__(self, pygame, screen, y = 0):
        self._pygame = pygame
        self._screen = screen
        self._img = pygame.image.load("assets/sprite/knife.png")
        self._img = pygame.transform.scale(self._img, (self._img.get_width() * 3, self._img.get_height() * 3))
        self._rect = self._img.get_rect()
        self._rect.x = screen.get_width() + self._rect.width
        self._rect.y = y

    def display(self):
        self._screen.blit(self._img, self._rect)

    def move(self, speed):
        self._rect.x -= speed

def mouseCollision(mousePos, utensilrect):
    return utensilrect._rect.collidepoint(mousePos)
