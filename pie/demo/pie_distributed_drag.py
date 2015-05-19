"""pieEngine - Pygame Engine
"""

import random

import pygame

from pie.entity.background import BackgroundImage
from pie.entity.primitive import Fill
from entity.base import Image
from pie.entity.composite import DistributedOnce
from pie.engine import Engine


class Demo(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)

        images = [Fill((20,20), center=(512,256),
                       fill_color=(random.randint(0,255),
                                   random.randint(0,255),
                                   random.randint(0,255))) for _ in range(10)]

        boxy = DistributedOnce(*images)

        self.boxy = boxy
        self.render_group.add(boxy)
        self.drag_handler.append(boxy)

    def update(self):
        Engine.update(self)
        self.boxy.update()


if __name__ == "__main__":
    pygame.init()

    sf = lambda: pygame.display.set_mode((1024, 512),
                                         pygame.RESIZABLE | pygame.SRCALPHA)

    bf = lambda: BackgroundImage(
                        pygame.image.load("assets/bg1.png").convert())

    game = Demo(screen_factory=sf, background_factory=bf)

    game.start()