"""pieEngine - Pygame Engine
"""
import time

import pygame
import pygame.math
import pygame.gfxdraw

from pie.engine import Engine


class Demo(Engine):
    def update(self):
        Engine.update(self)

        t1 = time.time()
        #pygame.gfxdraw.vline(self.draw_surface.surface, 512, 0, 512, (200,200,200))

        t1 = time.time()
        pygame.draw.line(self.draw_surface.surface, (220,220,220), (256,0), (256,512))
        pygame.draw.line(self.draw_surface.surface, (120,120,120), (255,0), (255,512))
        pygame.draw.line(self.draw_surface.surface, (120,120,120), (257,0), (257,512))


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1024, 512),
                                     pygame.DOUBLEBUF |
                                     pygame.ASYNCBLIT |
                                     pygame.RESIZABLE)
    clock = pygame.time.Clock()
    game = Demo(screen, clock)


    pygame.Rect((0,0),(0,0))
    print(pygame.math.Vector2(10,10) - pygame.math.Vector2(8,8))

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