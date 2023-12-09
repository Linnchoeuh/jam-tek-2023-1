from src.ColorPalette import *
from src.Mouse import Mouse

class Button:
    def __init__(self, pygame, screen, x = 0, y = 0, width = 100, height = 100, text = ""):
        self._pygame = pygame
        self._screen = screen
        self.strokeWidth = 5
        self.rect = self._pygame.Rect(0, 0, 0, 0)
        self.subRect = self._pygame.Rect(0, 0, 0, 0)
        self.text = ""
        self.setText(text)
        self.setRect(x, y, width, height)
        self.font = pygame.font.Font(None, 35)
        self.text_surface = self.font.render(self.text, True, GBACOLOR0)
        self.hover = False

    def setRect(self, x, y, width, height):
        self.rect = self._pygame.Rect(x, y, width, height)
        self.subRect = self._pygame.Rect(x + self.strokeWidth, y + self.strokeWidth, width - self.strokeWidth * 2, height - self.strokeWidth * 2)

    def setText(self, text):
        self.text = text

    def display(self):
        self._pygame.draw.rect(self._screen, GBACOLOR1, self.rect)
        if (self.hover):
            self._pygame.draw.rect(self._screen, GBACOLOR3, self.subRect)
        else:
            self._pygame.draw.rect(self._screen, GBACOLOR2, self.subRect)

        text_rect = self.text_surface.get_rect(center=self.rect.center)
        self._screen.blit(self.text_surface, text_rect)

    def isClicked(self, mouse: Mouse):
        self.hover = False
        if (self.rect.collidepoint(mouse.getPos())):
            self.hover = True
            if mouse.getButtonPressed()[0]:
                return True
        return False
