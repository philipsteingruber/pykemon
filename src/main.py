import logging
from sys import exit

import pygame.display
import pytmx

from entities import Player
from groups import AllSprites
from sprites import Sprite, AnimatedSprite
from support import *


class Game:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S')
        self.logger = logging.getLogger('main')

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('PYkémon')
        self.clock = pygame.time.Clock()

        self.all_sprites = AllSprites()

        self.tmx_maps = Game.import_maps()
        self.overworld_assets = Game.import_overworld_assets()

        self.player = None
        self.setup(self.tmx_maps['world'], 'house')

    @staticmethod
    def import_maps() -> dict[str: pytmx.TiledMap]:
        return {
            'world': pytmx.util_pygame.load_pygame('../data/maps/world.tmx'),
            'hospital': pytmx.util_pygame.load_pygame('../data/maps/hospital.tmx')}

    @staticmethod
    def import_overworld_assets() -> dict[str: list[pygame.Surface]]:
        return {
            'water': import_folder('..', 'graphics', 'tilesets', 'water'),
            'coast': coast_importer(24, 12, '..', 'graphics', 'tilesets', 'coast'),
            'characters': import_all_characters('..', 'graphics', 'characters')
        }

    def setup(self, tmx_map: pytmx.TiledMap, player_start_pos: str) -> None:
        for layer in ['Terrain', 'Terrain Top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player' and obj.properties['pos'] == player_start_pos:
                self.player = Player(
                    pos=(obj.x, obj.y),
                    frames=self.overworld_assets['characters']['player'],
                    groups=self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Water'):
            for x in range(int(obj.x), int(obj.x + obj.width), TILE_SIZE):
                for y in range(int(obj.y), int(obj.y + obj.height), TILE_SIZE):
                    AnimatedSprite((x, y), self.overworld_assets['water'], self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Coast'):
            terrain = obj.properties['terrain']
            side = obj.properties['side']
            AnimatedSprite((obj.x, obj.y), self.overworld_assets['coast'][terrain][side], self.all_sprites)

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            dt = self.clock.tick() / 1000

            self.all_sprites.update(dt)

            self.display_surface.fill('black')
            self.all_sprites.draw(self.player)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
