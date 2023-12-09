import random
import math

from src.Button import Button
from src.ColorPalette import *
from src.DisplayAction import DisplayAction
from src.Arrow import Arrow
from src.Timer import Timer
from src.Pause import Pause

class GreatSword:
    def __init__(self, pygame, screen, x = 0, y = 0):
        self._pygame = pygame
        self._screen = screen
        self._img = self._pygame.image.load("assets/img/great_sword.png")
        self._img = self._pygame.transform.scale(self._img, (200, 200))
        self._angle = 0
        self._x = x
        self._y = y
        self._slashSpeed = 30
        self._slashMaxAngle = 90
        self._cooldown = 0
        self._slashing = False
        self.reset()

    def reset(self):
        self._slashing = False
        self._angle = -30
        self._cooldown = 10

    def display(self):
        tmp = self._pygame.transform.rotate(self._img, -self._angle)
        self._screen.blit(tmp, (self._x, self._y))
        if (self._slashing):
            if self._angle < self._slashMaxAngle:
                self._angle += self._slashSpeed
            else:
                self._cooldown -= 1
            if (self._cooldown <= 0):
                self.reset()

    def setPos(self, x, y):
        self._x = x
        self._y = y

    def slash(self):
        self.reset()
        self._slashing = True


class MiniGameMonsterHunter:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen
        self.counter = 0
        self._arrows = []
        self._dissapearedArrow = []
        self._action = DisplayAction(pygame, screen, "Press arrow key!")
        self._msg = DisplayAction(pygame, screen, "Quest cleared!", "assets/sfx/quest_cleared.ogg")
        self._timer = Timer(pygame, screen, 10)
        self._pause = Pause(pygame, screen)

        self._gameChanged = False
        self._bg = None
        self._jagras = None
        self._jagrasEjectionList = []
        self._sword = GreatSword(pygame, screen, 0, 300)


    def loadScene(self, sceneManager):
        self._arrows = []
        self._dissapearedArrow = []
        self._jagrasEjectionList = []
        for i in range(5 + sceneManager.getDifficulty()):
            direction = random.randint(0, 3)
            self._arrows.append([direction,
                Arrow(self._pygame, self._screen, 0, 0, 50, 70, 10, direction * 90)
            ])
        self._action.reset()
        self._msg.reset()
        self._timer.reset()
        self._pause.reset()
        self._gameChanged = False
        self._bg = self._pygame.image.load("assets/img/mhw_bg.png")
        self._jagras = self._pygame.image.load("assets/img/jagras.png")
        self._jagras = self._pygame.transform.scale(self._jagras, (150, 150))
        self._hitSfx = [
            self._pygame.mixer.Sound("assets/sfx/hit1.ogg"),
            self._pygame.mixer.Sound("assets/sfx/hit2.ogg"),
            self._pygame.mixer.Sound("assets/sfx/hit3.ogg"),
            self._pygame.mixer.Sound("assets/sfx/hit4.ogg"),
            self._pygame.mixer.Sound("assets/sfx/hit5.ogg"),
            self._pygame.mixer.Sound("assets/sfx/hit6.ogg"),
        ]

    def unloadScene(self, sceneManager):
        self._bg = None
        self._hitSfx = []

    def run(self, sceneManager):
        events = sceneManager.getEvents()
        key = -1

        self._screen.blit(self._bg, (0, 0))
        for event in events:
            if event.type == self._pygame.KEYDOWN:
                if event.key == self._pygame.K_UP:
                    key = 0
                    break
                if event.key == self._pygame.K_RIGHT:
                    key = 1
                    break
                if event.key == self._pygame.K_DOWN:
                    key = 2
                    break
                if event.key == self._pygame.K_LEFT:
                    key = 3
                    break


        # Arrow display

        if len(self._arrows) > 0 and self._arrows[0][0] == key:
            self._sword.slash()
            self._arrows[0][1].setPos(550, 100)
            self._dissapearedArrow.append(self._arrows[0])
            self._arrows.pop(0)
            self._hitSfx[random.randint(0, len(self._hitSfx) - 1)].play()
            self._jagrasEjectionList.append([
                (150, 400), # Position
                random.randint(30, 100), # Speed
                random.randint(-170, 0), # Angle
                0 # Rotation
                ])

        self._pygame.draw.rect(self._screen, GBACOLOR0, (500, 50, 100, 100))
        offsetX = 0
        for arrow in self._arrows:
            arrow[1].setPos(offsetX + 550, 100)
            arrow[1].display()
            self._screen.blit(self._jagras, (offsetX + 150, 400))
            offsetX += 100
        for arrow in self._dissapearedArrow:
            arrow[1].dissapear()
            arrow[1].display()

        for jagras in self._jagrasEjectionList:
            jagras[0] = (jagras[0][0] + jagras[1] * math.cos(math.radians(jagras[2])), jagras[0][1] + jagras[1] * math.sin(math.radians(jagras[2])))
            jagras[3] += 60
            tmp = self._pygame.transform.rotate(self._jagras, jagras[3])
            self._screen.blit(tmp, jagras[0])
            if jagras[0][1] > 600:
                self._jagrasEjectionList.remove(jagras)


        # Sword display
        self._sword.display()



        if len(self._arrows) == 0:
            if self._msg.display() and not self._gameChanged:
                sceneManager.incrementDifficulty()
                sceneManager.incrementScore()
                sceneManager.changeScene("MiniGameMarioGalaxy")
                self._gameChanged = True
        elif self._timer.display():
            sceneManager.changeScene("LoseMenu")
        self._action.display()
        self._pause.display(sceneManager)
        sceneManager.displayScore()
