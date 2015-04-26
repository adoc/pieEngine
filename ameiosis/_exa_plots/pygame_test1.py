__author__ = 'coda'

import sys
import pygame
import pygame.time
from pygame.locals import *

from ameiosis.game import Blob

if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1024, 512))

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((20, 20, 20))

    if pygame.font:
        font = pygame.font.Font(None, 20)

    b1 = Blob(1)

    while 1:
        text = font.render("FPS %d" % clock.get_fps(), 1, (240, 240, 240))
        screen.blit(text, (8,8))
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                sys.exit(0)
        clock.tick(60)
        pygame.display.flip()

        screen.blit(background, (0, 0))
        b1.draw(screen, 10)
