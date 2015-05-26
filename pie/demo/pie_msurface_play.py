import pygame

from pie.entity import MSurfarray
from pie.entity.base import SpriteSurfarray


# Keep this minimal.
if __name__ == "__main__":
    pygame.init()
    s = pygame.display.set_mode((1024,512),0,32)

    i = pygame.image.load("assets/bg1.png").convert()

    # m = MSurfarray(i)
    # print(m.shape)
    # print(m.offset((100,100)))
    # m.blit_to(s)
    # pygame.display.flip()


    m = SpriteSurfarray(i)
    m.viewport.topleft = (100, 100)
    m.rect.topleft = (100, 100)
    m.blit_to(s)
    pygame.display.flip()