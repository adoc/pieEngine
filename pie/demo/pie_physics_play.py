"""

"""

import pygame
import pymunk

from pie.base import MRunnable
from pie.entity.animated import SurfaceSequence
from pie.entity.background import ParallaxBackground
from pie.entity.composite import DistributedAnimated
from pie.entity.image import Image
from pie.engine import Engine


class PhysicsDemo(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)

        # Setup bomber.
        bomber1_img = pygame.image.load("assets/bomber10000.png").convert_alpha()
        bomber1_img = pygame.transform.scale(bomber1_img, (32, 32))
        bombers = DistributedAnimated(*[Image(bomber1_img,
                                        rect_kwa={'center': (512,256)})
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

        # Physics
        self.__space = pymunk.Space()

        # Surprisingly fast load and transform of 360 PNG's for a ship animation.
        self.assets.animations.add_from_zip('ship1', "assets\\anim_ship1.zip",
                                            size=(128,128))

        ship1 = SurfaceSequence(self.assets.animations['ship1'], center=(512,256))

        self.add_render_plain(ship1)

    def update(self):
        Engine.update(self)
        self.bg_parallax.viewport.topleft = pygame.mouse.get_pos()

    def start(self):
        """
        """
        MRunnable.start(self)

        self.init()

        while not self.stopped:
            self.__space.step(1/self.target_fps)
            self.update()
            self.clear()
            self.throttle()
            self.render()

        return self.__end_state


# Keep this minimal.
if __name__ == "__main__":
    pygame.init()
    game = PhysicsDemo(pygame.display.set_mode((1024, 512), 0, 32),
                       non_static_background=True)

    game.start()