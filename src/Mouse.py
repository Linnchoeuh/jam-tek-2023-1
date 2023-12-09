from src.WindowConfig import *

class Mouse:
    def __init__(self, pygame):
        self._pygame = pygame
        self._screenW = SCREENW
        self._screenH = SCREENH
        self._prev = [False, False, False]
        self._current = [False, False, False]
        self._pressed = [False, False, False]
        self._released = [False, False, False]

    def update(self):
        self._prev = self._current
        self._current = self._pygame.mouse.get_pressed()
        for i in range(len(self._current)):
            self._pressed[i] = self._current[i] and not self._prev[i]
            self._released[i] = not self._current[i] and self._prev[i]

    def getButtonPressed(self):
        return self._pressed

    def getButtonReleased(self):
        return self._released

    def getButton(self):
        return self._current

    def scalePosition(self, w, h):
        self._screenW = w
        self._screenH = h

    def getPos(self):
        mousePos = self._pygame.mouse.get_pos()
        ratioW = self._screenH * SCREENRATIO
        h = SCREENH / self._screenH
        w = SCREENW / ratioW
        x = (mousePos[0] - ((self._screenW - ratioW) / 2)) * w
        y = mousePos[1] * h
        # print(x, y, ((self._screenW - ratioW) / 2))
        return [x, y]
