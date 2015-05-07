"""pieEngine - Pygame Engine
"""

import time

import pygame

from pie.entity import FillSpriteEntity, ImageSpriteEntity
from pie.engine import Engine


class Demo(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)
        boxy = (FillSpriteEntity((200,200),
                                        fill_color=(255,0,0),
                                        center=(512, 256)),
                FillSpriteEntity((200,200),
                                fill_color=(0,255,0),
                                center=(712, 312)),
                FillSpriteEntity((200,200),
                                fill_color=(0,0,255),
                                center=(312, 312)))

        self.render_group.add(boxy)
        self.drag_handler.extend(boxy)


if __name__ == "__main__":
    pygame.init()

    sf = lambda: pygame.display.set_mode((1024, 512),
                                     pygame.DOUBLEBUF |
                                     pygame.ASYNCBLIT |
                                     pygame.RESIZABLE)

    bf = lambda: ImageSpriteEntity(
                                pygame.image.load("assets/bg1.png").convert())

    game = Demo(screen_factory=sf, background_factory=bf)

    print(game.start())