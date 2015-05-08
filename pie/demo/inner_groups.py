"""pieEngine - Pygame Engine
"""


import pygame

from pie.entity.background import BackgroundImage
from pie.entity.primitive import Fill
from pie.entity.composite import Distributed
from pie.engine import Engine


class Demo(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)

        boxy = Distributed(Fill((20, 20),
                                 fill_color=(255, 0, 0),
                                 center=(512, 256)),
                            Fill((20, 20),
                                 fill_color=(0, 255, 0),
                                 center=(712, 312)),
                            Fill((20, 20),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)),
                            Fill((20, 20),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)),
                            Fill((20, 20),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)),
                            Fill((20, 20),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)),
                            Fill((20, 20),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)),
                            Fill((20, 20),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)),
                            Fill((20, 20),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)),
                            Fill((20, 20),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)),
                            Fill((20, 20),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)),
                            Fill((20, 20),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)),
                            Fill((20, 20),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)))
        self.boxy = boxy
        self.render_group.add(boxy)
        self.drag_handler.append(boxy)

    def update(self):
        Engine.update(self)
        self.boxy.update()



if __name__ == "__main__":
    pygame.init()

    sf = lambda: pygame.display.set_mode((1024, 512),
                                         pygame.RESIZABLE)

    bf = lambda: BackgroundImage(
        pygame.image.load("assets/bg1.png").convert())

    game = Demo(screen_factory=sf, background_factory=bf)

    game.start()