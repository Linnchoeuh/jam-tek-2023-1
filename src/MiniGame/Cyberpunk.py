from src.Button import Button
from src.ColorPalette import *
from src.DisplayAction import DisplayAction
from src.Arrow import Arrow
from src.Timer import Timer
from src.Pause import Pause
from src import ColorPalette

import random

NUM_LINES = 5
LINE_WIDTH = 20
LINE_SPACING = 150
LINE_COLOR = GBACOLOR1

note_height = 20
note_width = LINE_WIDTH * 2
note_color = GBACOLOR3

note_y = 0

class MiniGameCyberpunk:
    def __init__(self, pygame, screen):
        self._pygame = pygame
        self._screen = screen

        self._action = DisplayAction(self._pygame, self._screen, "Take the rythm!")
        self._msg = DisplayAction(self._pygame, self._screen, "Bravo!")

        self._timer = Timer(self._pygame, self._screen, 8)
        self._pause = Pause(self._pygame, self._screen)

        self._key_pressed = [False] * NUM_LINES
        self._gameChanged = False

    def loadScene(self, sceneManager):
        self._gameChanged = False
        self._timer.reset()
        self._action.reset()
        self._msg.reset()
        self._pause.reset()

        num_notes = 20

        self._notes = []
        for i in range(num_notes):
            note = {
                "line_index": random.randint(0, NUM_LINES - 1),
                "y": random.randint(-5000, -15),
                "has_appeared": False,
            }
            self._notes.append(note)
        self._note_speed = 5 + sceneManager.getDifficulty() // 10
        self._note_appeared = 0
        self._note_cleared = 0

        self._assigned_keys = ['Q', 'S', 'D', 'F', 'G']

        self._musical_notes = [
            self._pygame.mixer.Sound("assets/notes/do.ogg"),
            self._pygame.mixer.Sound("assets/notes/re.ogg"),
            self._pygame.mixer.Sound("assets/notes/mi.ogg"),
            self._pygame.mixer.Sound("assets/notes/fa.ogg"),
            self._pygame.mixer.Sound("assets/notes/sol.ogg"),
        ]

    def unloadScene(self, sceneManager):
        pass

    def run(self, sceneManager):
        events = sceneManager.getEvents()
        start_x = (self._screen.get_width() - (NUM_LINES - 1) * LINE_SPACING) // 2
        font = self._pygame.font.Font(None, 36)

        for event in events:
            if event.type == self._pygame.KEYDOWN:
                if event.key == self._pygame.K_q:
                    self.handle_input(0)
                elif event.key == self._pygame.K_s:
                    self.handle_input(1)
                elif event.key == self._pygame.K_d:
                    self.handle_input(2)
                elif event.key == self._pygame.K_f:
                    self.handle_input(3)
                elif event.key == self._pygame.K_g:
                    self.handle_input(4)

        for i in range(NUM_LINES):
            line_x = start_x + i * LINE_SPACING
            self._pygame.draw.line(self._screen, LINE_COLOR, (line_x, 0), (line_x, self._screen.get_height()), LINE_WIDTH)

            key_text = font.render(self._assigned_keys[i], True, GBACOLOR2)
            text_x = line_x - key_text.get_width() // 2
            text_y = self._screen.get_height() - 50
            self._screen.blit(key_text, (text_x, text_y))

        for note in self._notes:
            line_index = note["line_index"]
            note_x = start_x + line_index * LINE_SPACING - note_width // 2
            note_y = note["y"]
            note["y"] += self._note_speed

            if note["y"] >= self._screen.get_height() - 90 and not note["has_appeared"]:
                note["has_appeared"] = True
                self._note_appeared += 1

            if note["y"] >= self._screen.get_height():
                self._notes.remove(note)
                continue

            self._pygame.draw.rect(self._screen, note_color, (note_x, note_y, note_width, note_height))

        self._pygame.draw.rect(self._screen, GBACOLOR2, (75, self._screen.get_height() - 75, 650, LINE_WIDTH))

        self._pause.display(sceneManager)

        if self._timer.display():
            if self._note_cleared >= (self._note_appeared * 2) // 3:
                self._msg.display()
                if not self._gameChanged:
                    sceneManager.nextGame()
                    self._gameChanged = True
            else:
                sceneManager.changeScene("LoseMenu")

        self._action.display()

    def handle_input(self, line_index):
        for note in self._notes:
            if note["line_index"] == line_index:
                if note["y"] > self._screen.get_height() - 75 - LINE_WIDTH:
                    self._notes.remove(note)
                    self._note_cleared += 1
                    self._musical_notes[line_index].play()
                    return True
        return False
