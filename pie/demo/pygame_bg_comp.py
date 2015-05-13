import time
import numpy
import pygame
from pie.math import sub_size


if __name__ == "__main__":
    pygame.init()
    pygame.surfarray.use_arraytype('numpy')

    def dodge(front, back):
        result=back*256.0/(256.0-front)
        result[result>255]=255
        result[front==255]=255
        return result.astype('uint8')

    info = pygame.display.Info()

    screen = pygame.display.set_mode((512, 512))
    clock = pygame.time.Clock()

    bg1 = pygame.Surface((512,512))
    bg1.fill((0,0,0))

    i = pygame.image.load("assets/composite/bg1.png").convert()
    bg1.blit(i, (0,0))

    bg2 = pygame.image.load("assets/composite/bg2_cloud_mult.png").convert()

    bg1_a = pygame.surfarray.array3d(bg1)
    bg2_a = pygame.surfarray.array3d(bg2)

    running = True
    while running:
        clock.tick(60)
        print(clock.get_fps())

        #screen.fill((0,0,0))

        pygame.surfarray.blit_array(screen, dodge(bg2_a, bg1_a))

        pygame.display.flip()

        if pygame.event.get(pygame.QUIT):
            running = False
        pygame.event.clear()


