import pygame.display

from settings import *
from sys import exit
import pytmx
from typing import Tuple
from sprites import Sprite
from entities import Player


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('PYkémon')

        self.all_sprites = pygame.sprite.Group()

        self.tmx_maps = Game.import_maps()
        self.setup(self.tmx_maps['world'], 'house')

    @staticmethod
    def import_maps() -> dict[str: pytmx.TiledMap]:
        return {'world': pytmx.util_pygame.load_pygame('../data/maps/world.tmx')}

    def setup(self, tmx_map: pytmx.TiledMap, player_start_pos: str) -> None:
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                self.all_sprites.draw(self.display_surface)
                pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
