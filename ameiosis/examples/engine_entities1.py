import time
import pygame
from pygame.locals import *

from ameiosis.engine.entities import FillEntity


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1024, 512),
                                     DOUBLEBUF | ASYNCBLIT | RESIZABLE)
    clock = pygame.time.Clock()

    bg = FillEntity(screen.get_size(), fill_color=(255,0,0))
    bg.surface_convert(screen)
    bg.update()
    screen.blit(*bg.present())

    box = FillEntity((512,256), fill_color=(0,255,0),
                     center=screen.get_rect().center)
    box.surface_convert(screen)
    box.update()
    screen.blit(*box.present())

    pygame.display.flip()