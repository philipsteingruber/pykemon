import pygame.sprite

from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf: pygame.Surface, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)


class AnimatedSprite(Sprite):
    def __init__(self, pos, frames, groups):
        self.frame_index = 0
        self.frames = frames

        super().__init__(pos, frames[0], groups)

    def update(self, dt) -> None:
        self.animate(dt)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.frame_index %= len(self.frames)
        self.image = self.frames[int(self.frame_index)]
