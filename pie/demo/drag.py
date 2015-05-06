"""pieEngine - Pygame Engine
"""

import time

import pygame
import pygame.gfxdraw

from pie.entity import FillSurfaceEntity
from pie.engine import Engine


class Demo(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)
        self.__boxy = FillSurfaceEntity((200,200),
                                        fill_color=(255,0,0),
                                        center=(512, 256))

        # This is all that's needed to make an entity draggable.
        self.drag_handler.append(self.__boxy)

    def draw(self):
        Engine.draw(self)
        self.append_blit(self.__boxy.present)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1024, 512),
                                     pygame.DOUBLEBUF |
                                     pygame.ASYNCBLIT |
                                     pygame.RESIZABLE)
    clock = pygame.time.Clock()
    game = Demo(screen, clock)

    while not game.stopped:
        t1 = time.time()
        game.buffer()
        game.update()
        game.draw()
        game.render()
        game.draw_debug(tick_time=time.time() - t1)