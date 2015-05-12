import time
import numpy
import pygame
from pie.math import vect_diff

import pie._pygame.sprite
from pie.entity.background import ParallaxBackground
from pie.entity import MSurface
from pie.entity.image import Image
from pie.entity.composite import DistributedAnimated
from pie.engine import Engine



class ParallaxDemo(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)

        # Setup bomber.
        bomber1_img = pygame.image.load("assets/bomber10000.png").convert_alpha()
        bomber1_img = pygame.transform.scale(bomber1_img, (32, 32
                                                           ))
        bombers = DistributedAnimated(*[Image(bomber1_img,
                                        rect_kwa={'center':(512,256)})
                                            for _ in range(10)])

        self.bg_parallax = ParallaxBackground(
            viewport=pygame.Rect((0, 0), (1024, 512)))
        #viewport =
        # Blitted as BG.
        bg_nr = Image(
            pygame.image.load("assets/composite/sf1_bg_close.png").convert())
        # Blitted as first ADDed.
        bg_mid = Image(
            pygame.image.load("assets/composite/sf1_bg_med.png").convert(),
            blit_flags=pygame.BLEND_RGBA_ADD)
        # Blitted as second ADDed.
        bg_far = Image(
            pygame.image.load("assets/composite/sf1_bg_far.png").convert(),
            blit_flags=pygame.BLEND_RGBA_ADD)

        bg_nr.parallax_offset = 1
        bg_mid.parallax_offset = .4
        bg_far.parallax_offset = .33

        self.bg_parallax.add(bg_nr, bg_mid, bg_far)

        self.add_render_plain(self.bg_parallax)
        self.add_render_plain(bombers)

    def update(self):
        Engine.update(self)
        self.bg_parallax.viewport.topleft = pygame.mouse.get_pos()


if __name__ == "__main__":
    pygame.init()

    info = pygame.display.Info()
    screen = pygame.display.set_mode((1024, 512), 0, 32)


    game = ParallaxDemo(screen)
    game.start()