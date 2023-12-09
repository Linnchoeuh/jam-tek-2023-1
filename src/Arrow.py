from src.ColorPalette import *
import pygame

class Arrow:
    def __init__(self, pygame, screen, x = 0, y = 0, size = 50, length = 100, thickness = 5, angle = 0):
        self._pygame = pygame
        self._screen = screen
        self._x = x
        self._y = y
        self._size = size
        self._length = length
        self._thickness = thickness
        self._angle = angle
        self._arrow = None
        self._oppacityDecrease = 30

        self.reset()
        self.render()

    def reset(self):
        self._oppacity = 255

    def render(self):
        self._arrow = pygame.surface.Surface((self._size + self._thickness * 2, self._length + self._thickness * 2))
        width = self._arrow.get_width()
        height = self._arrow.get_height()
        self._arrow.set_colorkey((0,0,0))  # Black colors will not be blit.
        middle = width / 2
        left = (middle) - (self._size / 2)
        right = (middle) + (self._size / 2)
        pygame.draw.line(self._arrow, GBACOLOR1, (left, self._thickness + self._size), (middle, self._thickness), width=self._thickness * 2)
        pygame.draw.line(self._arrow, GBACOLOR1, (middle, self._thickness), (right, self._thickness + self._size), width=self._thickness * 2)
        pygame.draw.line(self._arrow, GBACOLOR1, (middle, self._thickness), (middle, height), width=self._thickness * 2)
        pygame.draw.line(self._arrow, GBACOLOR3, (left, self._thickness + self._size), (middle, self._thickness), width=self._thickness)
        pygame.draw.line(self._arrow, GBACOLOR3, (middle, self._thickness), (right, self._thickness + self._size), width=self._thickness)
        pygame.draw.line(self._arrow, GBACOLOR3, (middle, self._thickness), (middle, height), width=self._thickness - 1)


    def setPos(self, x, y):
        self._x = x
        self._y = y

    def setSize(self, size):
        self._size = size
        self.render()

    def setLength(self, length):
        self._length = length
        self.render()

    def setThickness(self, thickness):
        self._thickness = int(thickness)
        self.render()

    def setRotation(self, angle):
        self._angle = angle

    def display(self):
        if (self._oppacity > 0):
            tmp = pygame.transform.rotate(self._arrow, -self._angle)
            if (self._oppacity > 0 and self._oppacity < 255):
                tmp.set_alpha(self._oppacity)
                scale = 1 + (255 - self._oppacity) / 255
                tmp = self._pygame.transform.scale(tmp, (int(tmp.get_width() * scale), int(tmp.get_height() * scale)))
                self._oppacity -= self._oppacityDecrease
            pos = (self._x - (tmp.get_width() / 2), self._y - (tmp.get_height() / 2))
            self._screen.blit(tmp, pos)

    def dissapear(self):
        if (self._oppacity == 255):
            self._oppacity -= self._oppacityDecrease
        return (self._oppacity <= 0)
