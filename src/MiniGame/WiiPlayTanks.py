import random
import math

from src.Button import Button
from src.ColorPalette import *
from src.DisplayAction import DisplayAction
from src.Animation import Animation
from src.Timer import Timer
from src.Pause import Pause

class Missile:
    def __init__(self, pygame, screen, reboundSfx, explosionSfx, explosionImg, x, y, angle, tag = 0, color = GBACOLOR3, speed = 5):
        self._pygame = pygame
        self._screen = screen

        self._x = x
        self._y = y
        self._angle = angle
        self._tag = tag
        self._color = color
        self._nbFrame = 17

        self._exploding = 0
        self._rebound = 1
        self._speed = speed
        self._reboundSfx = reboundSfx
        self._explosionSfx = explosionSfx
        self._explosion = Animation(pygame.transform.scale(explosionImg, (21 * self._nbFrame, 30)), self._nbFrame, 1)

    def move(self):
        if self._rebound < 0 and self._exploding == 0:
            self._exploding = 1
            return
        if self._exploding != 0:
            return
        self._x += math.cos(math.radians(self._angle)) * self._speed
        self._y += math.sin(math.radians(self._angle)) * self._speed

        if (self._x < 0 or self._x > self._screen.get_width()):
            self._rebound -= 1
            self._angle = 180 - self._angle
            if self._rebound >= 0:
                self._reboundSfx.play()
        if (self._y < 0 or self._y > self._screen.get_height()):
            self._rebound -= 1
            self._angle = 360 - self._angle
            if self._rebound >= 0:
                self._reboundSfx.play()

    def display(self) -> bool:
        if self._exploding == 0:
            self._pygame.draw.circle(self._screen, self._color, (int(self._x), int(self._y)), 5)
            return True
        if self._exploding == 1:
            if self._nbFrame == 17:
                self._explosionSfx.play()
            self._nbFrame -= 1
            self._explosion.update()
            self._explosion.draw(self._screen, int(self._x), int(self._y))
            if self._nbFrame <= 1:
                self._exploding = 2
            return True
        return False

    def explode(self):
        self._exploding = 1

    def getPos(self):
        return (self._x, self._y)

    def getExploding(self):
        return self._exploding

class Tank:
    def __init__(self, pygame, screen, x = 0, y = 0, speed = 10, tag = 0, movable = True, color1 = GBACOLOR1, color2 = GBACOLOR3):
        self._pygame = pygame
        self._screen = screen
        self._x = x
        self._y = y
        self._speed = speed
        self._angle = 0
        self._tag = tag
        self._color1 = color1
        self._color2 = color2
        self._coolDown = 0
        self._coolDownMax = 24
        self._exploding = 0
        self._nbFrame = 17

        self._baseSurf = None
        self._canonSurf = None
        self._topSurf = None
        self._movable = movable

        self._targetMovement = 0

        self._tankFireSfx = pygame.mixer.Sound("assets/sfx/tank_fire.ogg")
        self._reboundSfx = pygame.mixer.Sound("assets/sfx/rebound.ogg")
        self._explosionSfx = pygame.mixer.Sound("assets/sfx/explosion.ogg")
        self._bulletExplosionSfx = pygame.mixer.Sound("assets/sfx/bullet_explosion.ogg")
        self._explosionImg = pygame.image.load("assets/sprite/explosion.png")
        self._explosion = Animation(pygame.transform.scale(self._explosionImg, (91 * self._nbFrame, 130)), self._nbFrame, 1)

        self.render()



    def render(self):
        self._baseSurf = self._pygame.Surface((60, 70))
        self._baseSurf.fill(GBACOLOR0)
        self._pygame.draw.rect(self._baseSurf, self._color1, (7, 0, 45, 70))

        canonLen = 50
        self._canonSurf = self._pygame.Surface((canonLen * 2, 20))
        self._pygame.draw.line(self._canonSurf, GBACOLOR0, (canonLen, 10), (canonLen * 2, 10), 20)
        self._pygame.draw.line(self._canonSurf, self._color2, (canonLen, 10), (canonLen * 2, 10), 8)

        self._topSurf = self._pygame.Surface((50, 50))
        tmp = (25, 25)
        self._pygame.draw.circle(self._topSurf, GBACOLOR0, tmp, 22)
        self._pygame.draw.circle(self._topSurf, self._color2, tmp, 15)

        # self._baseSurf.set_colorkey((0,0,0))
        self._canonSurf.set_colorkey((0,0,0))
        self._topSurf.set_colorkey((0,0,0))

    def display(self):
        if self._exploding == 0:
            x = self._x - self._baseSurf.get_width() / 2
            y = self._y - self._baseSurf.get_height() / 2
            self._screen.blit(self._baseSurf, (x, y))
            tmp = self._pygame.transform.rotate(self._canonSurf, -self._angle)
            self._screen.blit(tmp, (self._x - (tmp.get_width() / 2), self._y - (tmp.get_height() / 2)))
            self._screen.blit(self._topSurf, (self._x - (self._topSurf.get_width() / 2), self._y - (self._topSurf.get_height() / 2)))
            return True
        if self._exploding == 1:
            if self._nbFrame == 17:
                self._explosionSfx.play()
            self._nbFrame -= 1
            self._explosion.update()
            self._explosion.draw(self._screen, int(self._x), int(self._y))
            if self._nbFrame <= 1:
                self._exploding = 2
            return True
        return False


    def setAngle(self, angle):
        self._angle = angle

    def getPosition(self):
        return (self._x, self._y)

    def moveY(self, direction):
        if not self._movable:
            return
        if (direction < 0 and self._y - (self._baseSurf.get_height() / 2) > 0):
            self._y -= self._speed
        elif (direction > 0 and self._y + (self._baseSurf.get_height() / 2) < self._screen.get_height()):
            self._y += self._speed

    def getSpeed(self):
        return self._speed

    def shoot(self):
        if self._exploding != 0:
            return None
        self._tankFireSfx.play()
        return Missile(self._pygame, self._screen, self._reboundSfx, self._bulletExplosionSfx, self._explosionImg, self._x, self._y, self._angle, self._tag, self._color2)

    def checkCollision(self, missiles):
        if self._exploding != 0:
            return False
        left = self._x - self._baseSurf.get_width() / 2
        right = self._x + self._baseSurf.get_width() / 2
        top = self._y - self._baseSurf.get_height() / 2
        bottom = self._y + self._baseSurf.get_height() / 2
        for missile in missiles:
            if missile.getExploding() == 0 and missile._tag != self._tag:
                if (missile.getPos()[0] > left and missile.getPos()[0] < right and
                    missile.getPos()[1] > top and missile.getPos()[1] < bottom):
                    self._explosionSfx.play()
                    missile.explode()
                    self._exploding = 1
                    return True
        return False

    def autoPlay(self, targetPos, difficulty):
        if self._exploding != 0:
            return None
        dx = targetPos[0] - self._x
        dy = targetPos[1] - self._y
        angle = math.degrees(math.atan2(dy, dx))
        self.setAngle(angle)

        if self._coolDown <= 0:
            self._coolDown = random.randint(self._coolDownMax * 4 - difficulty, self._coolDownMax * 8 - difficulty)
            return self.shoot()
        else:
            self._coolDown -= 1

        if self._targetMovement > 0:
            self._targetMovement -= 1
        elif self._targetMovement < 0:
            self._targetMovement += 1
        if self._targetMovement == 0:
            self._targetMovement = random.randint(-50, 50)
        self.moveY(self._targetMovement)

        return None




class MiniGameWiiPlayTanks:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen
        self._action = DisplayAction(pygame, screen, "Aim and shot by clicking!", "assets/sfx/start_trumpet.ogg")
        self._msg = DisplayAction(pygame, screen, "Victory!", "assets/sfx/win_trumpet.ogg")
        self._timer = Timer(pygame, screen, 30)
        self._pause = Pause(pygame, screen)

        self._tank = None
        self._tanks = []
        self._bg = None
        self._missiles = []
        self._gameChanged = False

    def loadScene(self, sceneManager):
        self._tank = Tank(self._pygame, self._screen, 200, self._screen.get_size()[1] / 2, 3)
        self._gameChanged = False
        self._tanks = []
        for i in range(sceneManager.getDifficulty() // 2 + 3):
            self._tanks.append(Tank(self._pygame, self._screen, \
                random.randint(0, 3) * 70 + 550, \
                random.randint(0, (self._screen.get_size()[1] / 100) - 2) * 100 + 100, \
                1, 1, (random.randint(0, 9) < sceneManager.getDifficulty()), GBACOLOR3, GBACOLOR1))
        self._missiles = []
        self._action.reset()
        self._msg.reset()
        self._timer.reset()
        self._pause.reset()

        self._bg = self._pygame.image.load("assets/img/parquet.png")

    def unloadScene(self, sceneManager):
        self._bg = None

    def run(self, sceneManager):
        mousePos = sceneManager._mouse.getPos()

        # bg
        self._screen.blit(self._bg, (0, 0))

        # player tank
        # Calculate the angle between the tank's canon and the mouse position
        tankPos = self._tank.getPosition()
        dx = mousePos[0] - tankPos[0]
        dy = mousePos[1] - tankPos[1]
        angle = math.degrees(math.atan2(dy, dx))
        self._tank.setAngle(angle)

        if abs(tankPos[1] - mousePos[1]) > self._tank.getSpeed():
            self._tank.moveY(mousePos[1] - tankPos[1])

        self._tank.checkCollision(self._missiles)
        self._tank.display()

        if self._tank._coolDown > 0:
            self._tank._coolDown -= 1

        if (sceneManager._mouse.getButtonPressed()[0] and self._tank._coolDown <= 0):
            tmp = self._tank.shoot()
            if tmp != None:
                self._missiles.append(tmp)
                self._tank._coolDown = self._tank._coolDownMax

        # enemy tanks

        for tank in self._tanks:
            tank.checkCollision(self._missiles)
            tank.display()
            bullet = tank.autoPlay(tankPos, sceneManager.getDifficulty())
            if bullet != None:
                self._missiles.append(bullet)
        for tank in self._tanks:
            if tank._exploding == 2:
                self._tanks.remove(tank)

        # missiles handling

        for missile in self._missiles:
            missile.move()
            if not missile.display():
                self._missiles.remove(missile)

        self._action.display()
        if len(self._tanks) == 0:
            self._missiles = []
            if self._msg.display() and not self._gameChanged:
                sceneManager.nextGame()
                self._gameChanged = True
        elif self._timer.display() or self._tank._exploding > 1:
            sceneManager.changeScene("LoseMenu")
        self._pause.display(sceneManager)
        sceneManager.displayScore()
