import pygame.display

from settings import *
from sys import exit
import pytmx


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('PYkémon')

    @staticmethod
    def import_assets() -> dict[str: pytmx.TiledMap]:
        return {'world': pytmx.util_pygame.load_pygame('../data/maps/world.tmx')}

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
