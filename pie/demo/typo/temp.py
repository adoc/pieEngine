import time
import pygame

from pie.typo import Font


if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    font = pygame.font.SysFont('helvetica', 20, italic=True)

    s = pygame.display.set_mode((1024, 512), 0 , 32)
    c = pygame.time.Clock()
    f = font.render("This is a doggypaws!!!!", True, (255,255,255))

    while (True):
        s.fill((0,0,0))
        s.blit(f, (100,100))
        pygame.display.flip()
        c.tick(60)
