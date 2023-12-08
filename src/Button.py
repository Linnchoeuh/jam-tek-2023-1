from src.ColorPalette import *

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
        self.font = pygame.font.Font(None, 24)
        self.text_surface = self.font.render(self.text, True, GBACOLOR0)

    def setRect(self, x, y, width, height):
        self.rect = self._pygame.Rect(x, y, width, height)
        self.subRect = self._pygame.Rect(x + self.strokeWidth, y + self.strokeWidth, width - self.strokeWidth * 2, height - self.strokeWidth * 2)

    def setText(self, text):
        self.text = text

    def display(self):
        self._pygame.draw.rect(self._screen, GBACOLOR1, self.rect)
        self._pygame.draw.rect(self._screen, GBACOLOR2, self.subRect)

        text_rect = self.text_surface.get_rect(center=self.rect.center)
        self._screen.blit(self.text_surface, text_rect)

    def isClicked(self, events):
        for event in events:
            if event.type == self._pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return True
        return False
