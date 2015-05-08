import pygame
from pygame.locals import *

from pie.entity import FillSurfaceEntity


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((1024, 512),
                                     DOUBLEBUF | ASYNCBLIT | RESIZABLE)
    clock = pygame.time.Clock()

    bg = FillSurfaceEntity(screen.get_size(), fill_color=(255,0,0))
    bg.convert_ip(screen)
    bg.update()
    screen.blit(*bg.present())

    box = FillSurfaceEntity((512,256), fill_color=(0,255,0),
                     center=screen.get_rect().center)
    box.convert_ip(screen)
    box.update()
    screen.blit(*box.present())

    pygame.display.flip()