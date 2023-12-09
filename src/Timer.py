from src.ColorPalette import *

import time

class Timer:
    def __init__(self, pygame, screen, duration = 5):
        self._pygame = pygame
        self._screen = screen
        self._duration = duration
        self._startTime = time.time()
        self._currentTime = time.time()
        self._height = 10
        self.reset()

    def reset(self):
        self._startTime = time.time()


    def display(self) -> bool:
        """Display the timer

        Returns:
            bool: _description_
        """
        timing = time.time() - self._startTime
        if timing >= self._duration:
            return True
        rect = self._pygame.Rect(0, self._screen.get_height() - self._height, self._screen.get_width() * (1 - (timing / self._duration)), self._height)
        if (self._duration - timing) <= 2 and (self._duration - timing) % 0.4 < 0.2:
            self._pygame.draw.rect(self._screen, GBACOLOR1, rect)
        else:
            self._pygame.draw.rect(self._screen, GBACOLOR3, rect)
        return False
