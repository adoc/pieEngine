import time

import pygame

from ameiosis.game_proto import Ameosis


if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1024, 512))

    game = Ameosis(screen, clock)

    while not game.done:
        t1 = time.time()
        game.buffer()
        game.handle_events()
        game.update()
        game.draw()
        game.draw_debug(tick_time=time.time() - t1)