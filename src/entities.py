from settings import *


class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups):
        super().__init__(groups)

        self.frame_index = 0
        self.frames = frames
        self.facing_direction = 'down'

        self.direction = vector()
        self.movement_speed = 250

        self.image = self.frames[self.facing_direction][0]
        self.rect = self.image.get_frect(center=pos)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        state = self.get_state()
        self.image = self.frames[state][int(self.frame_index) % len(self.frames[state])]

    def get_state(self):
        moving = bool(self.direction)
        if moving:
            if self.direction.x > 0:
                self.facing_direction = 'right'
            elif self.direction.x < 0:
                self.facing_direction = 'left'
            elif self.direction.y > 0:
                self.facing_direction = 'down'
            elif self.direction.y < 0:
                self.facing_direction = 'up'

            return self.facing_direction
        else:
            return f'{self.facing_direction}_idle'


class Player(Entity):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()

        if keys[pygame.K_UP]:
            input_vector.y += -1
        if keys[pygame.K_DOWN]:
            input_vector.y += 1
        if keys[pygame.K_LEFT]:
            input_vector.x += -1
        if keys[pygame.K_RIGHT]:
            input_vector.x += 1
        self.direction = input_vector

    def move(self, dt):
        self.rect.center += self.direction * self.movement_speed * dt

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
