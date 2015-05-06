"""pieEngine - Pygame Engine
"""

import time

import pygame
import pygame.gfxdraw

from pie.engine import Engine


class Demo(Engine):
    def update(self):
        Engine.update(self)


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1024, 512),
                                     pygame.DOUBLEBUF |
                                     pygame.ASYNCBLIT |
                                     pygame.RESIZABLE)
    clock = pygame.time.Clock()
    game = Demo(screen, clock)

    # game._debug_lines.append(("Loading and Processing images...",
    #                                 1, (240, 240, 240)))
    # game.draw_debug()
    # game.buffer()
    # game.assets.animations.add_from_zip('bomber1', "assets\\bomber1.zip",
    #                                     size=(64,64))

    while not game.stopped:
        t1 = time.time()
        game.buffer()
        game.update()
        game.draw()
        game.render()
        game.draw_debug(tick_time=time.time() - t1)