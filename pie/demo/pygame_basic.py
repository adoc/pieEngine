import time
import pygame
from pie.math import sub_size


if __name__ == "__main__":
    pygame.init()

    # print(pygame.display.get_wm_info())
    # print(pygame.display.list_modes())

    info = pygame.display.Info()
    print(info)
    print(info.current_w)

    a = pygame.Rect((0,0), (100,100))
    b = pygame.Rect((0,0), (50,50))

    print(sub_size(a.size, b.size))


    screen = pygame.display.set_mode((info.current_w//2, info.current_h//2))

    bg = pygame.image.load("assets/bg1.png").convert()
    r = bg.get_rect(center=(info.current_w//4, info.current_h//4))


    screen.blit(bg, r)

    pygame.display.flip()

    pygame.time.delay(5000)


