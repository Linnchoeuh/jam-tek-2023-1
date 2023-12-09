from src.ColorPalette import *

class DisplayAction:
    def __init__(self, pygame, screen, text = "Play!"):
        self._pygame = pygame
        self._screen = screen
        self.font = pygame.font.Font(None, 80)
        self.fastSpeed = 40
        self.slowSpeed = 3
        self.slowZone = 150
        self.pos = 0
        self.offset = 0
        self.text = ""
        self.yPos = -1
        self.setText(text)
        self.reset()

    def reset(self):
        self.pos = 0

    def setYPos(self, y = -1):
        self.yPos = y

    def setText(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, GBACOLOR3)
        self.offset = self.text_surface.get_width()

    def display(self):
        pos = self.pos - self.offset
        if (pos < self._screen.get_width()):
            tmp = pos + self.offset / 2
            if (tmp >= self._screen.get_width() / 2 - self.slowZone / 2 and tmp <= self._screen.get_width() / 2 + self.slowZone / 2):
                self.pos += self.slowSpeed
            else:
                self.pos += self.fastSpeed
            text_rect = self.text_surface.get_rect(center=self._screen.get_rect().center)
            text_rect.x = pos
            if (self.yPos >= 0):
                text_rect.y = self.yPos
            self._screen.blit(self.text_surface, text_rect)
            return False
        return True
