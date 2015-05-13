"""

"""

import pygame

from pie.entity.background import ParallaxBackground
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

        self.bg_parallax.add(
            Image(
            pygame.image.load("assets/composite/sf1_bg_med2.png").convert(),
            parallax_distance=3),
            Image(
            pygame.image.load("assets/composite/sf1_bg_far.png").convert(),
            blit_flags=pygame.BLEND_RGBA_ADD,
            parallax_distance=11),
            Image(
            pygame.image.load("assets/composite/sf1_bg_med1.png").convert(),
            blit_flags=pygame.BLEND_RGBA_ADD,
            parallax_distance=6),
            Image(
            pygame.image.load("assets/composite/sf1_bg_near.png").convert(),
            blit_flags=pygame.BLEND_RGBA_ADD,
            parallax_distance=1))

        self.add_render_plain(self.bg_parallax)
        self.add_render_plain(bombers)

    def update(self):
        Engine.update(self)
        self.bg_parallax.viewport.topleft = pygame.mouse.get_pos()


if __name__ == "__main__":
    pygame.init()

    game = ParallaxDemo(pygame.display.set_mode((1024, 512), 0, 32),
                        non_static_background=True)
    game.start()