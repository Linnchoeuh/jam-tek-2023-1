import pygame

class Animation(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet, nbrFrames, animation_speed):
        super().__init__()
        self.sprite_sheet = sprite_sheet
        self.nbrFrames = nbrFrames
        self.animation_speed = animation_speed
        self.frame_width = sprite_sheet.get_width() / nbrFrames
        self.frame_height = sprite_sheet.get_height()
        self.image = pygame.Surface((self.frame_width, self.frame_height))
        self.rect = self.image.get_rect()
        self.current_frame = 0
        self.animation_speed = 5
        self.animation_counter = 0
        self.frames = self.load_frames()

    def load_frames(self):
        frames = []
        for j in range(self.nbrFrames):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (j * self.frame_width, 0, self.frame_width, self.frame_height))
            frames.append(frame)
        return frames

    def update(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter % self.animation_speed == 0:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def draw(self, screen, x = 0, y = 0):
        screen.blit(self.image, (x - self.frame_width / 2, y - self.frame_height / 2))
