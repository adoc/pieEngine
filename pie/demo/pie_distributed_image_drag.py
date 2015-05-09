"""pieEngine - Pygame Engine
"""

from threading import Timer

import pygame

from pie.entity.background import BackgroundImage
from pie.entity.primitive import Fill
from pie.entity.image import Image
from pie.entity.composite import DistributedOnce
from pie.engine import Engine


class Demo(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)

        image_surf = pygame.image.load("assets/bomber10000.png").convert_alpha()
        image_surf = pygame.transform.scale(image_surf, (64,64))
        images = [Image(image_surf, center=(512,256)) for _ in range(10)]

        boxy = DistributedOnce(*images)

        self.boxy = boxy

        self.render_group.add(boxy) # Adding a group here, but pygame breaks this down in to individual sprites, therefore breaking any sub_group functionality.
        self.drag_handler.append(boxy)

    def update(self):
        Engine.update(self)
        self.boxy.update()





if __name__ == "__main__":
    pygame.init()

    sf = lambda: pygame.display.set_mode((1024, 512),
                                         pygame.RESIZABLE)

    bf = lambda: BackgroundImage(
                        pygame.image.load("assets/bg2.png").convert())



    game = Demo(screen_factory=sf, background_factory=bf)
    t = Timer(10, game.stop)
    t.start()

    game.start()

    t.join()