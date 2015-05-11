import time
import numpy
import pygame
from pie.math import vect_diff

from pie.entity.image import Image


if __name__ == "__main__":
    pygame.init()
    pygame.surfarray.use_arraytype('numpy')

    info = pygame.display.Info()

    screen = pygame.display.set_mode((1024, 512))
    clock = pygame.time.Clock()

    bg_far = pygame.image.load("assets/composite/sf1_bg_far.png").convert()
    bg_mid = pygame.image.load("assets/composite/sf1_bg_med.png").convert()
    bg_nr = pygame.image.load("assets/composite/sf1_bg_close.png").convert()

    far_vrect = pygame.Rect((0, 0), (1024, 512))
    mid_vrect = pygame.Rect((0, 0), (1024, 512))
    nr_vrect = pygame.Rect((0, 0), (1024, 512))

    running = True
    while running:
        clock.tick(60)
        if pygame.event.get(pygame.QUIT):
            running = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            nr_vrect.topleft = pos[0]*1, pos[1]*1
            mid_vrect.topleft = pos[0]*.66, pos[1]*.66
            far_vrect.topleft = pos[0]*.33,  pos[1]*.33

        pygame.event.clear()

        print(clock.get_fps())

        screen.blit(bg_mid, (0,0), mid_vrect)
        screen.blit(bg_far, (0,0), far_vrect, special_flags=pygame.BLEND_RGBA_ADD)
        screen.blit(bg_nr, (0,0), nr_vrect, special_flags=pygame.BLEND_RGBA_ADD)

        pygame.display.flip()




