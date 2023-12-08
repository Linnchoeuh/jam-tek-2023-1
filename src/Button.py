class Button:
    def __init__(self, pygame, screen, x = 0, y = 0, width = 100, height = 100, text = ""):
        self._pygame = pygame
        self._screen = screen
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.Font(None, 24)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))

    def setRect(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def setText(self, text):
        self.text = text

    def display(self):
        self._pygame.draw.rect(self._screen, (255, 255, 255), self.rect)

        text_rect = self.text_surface.get_rect(center=self.rect.center)
        self._screen.blit(self.text_surface, text_rect)

    def isClicked(self, events):
        for event in events:
            if event.type == self._pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return True
        return False
