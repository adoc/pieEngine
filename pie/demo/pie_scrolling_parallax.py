
import pygame

from pie.engine import Engine
from pie.entity.primitive import Image, ImageSurfarray, BlurredImage
from pie.entity.background import ScrollingParallaxBackground, RepeatingProjectedImage


class ScrollingBgDemo(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)

        self.bg = ScrollingParallaxBackground(
            # lambda: Image(
            # pygame.image.load("assets/composite/sf1_bg_med2.png").convert(),
            # parallax_distance=3),
            # lambda: Image(
            # pygame.image.load("assets/composite/sf1_bga_near.png").convert_alpha(),
            # parallax_distance=40),
            # lambda: Image(
            # pygame.image.load("assets/composite/sf1_bga_near.png").convert_alpha(),
            # parallax_distance=30),
            lambda: Image(
            pygame.image.load("assets/composite/sf1_bga_neb1.png").convert(),
            blit_flags=pygame.BLEND_RGBA_ADD,
            parallax_distance=20),
            lambda: Image(
            pygame.image.load("assets/composite/sf1_bga_neb2.png").convert(),
            blit_flags=pygame.BLEND_RGBA_ADD,
            parallax_distance=10),
            lambda: Image(
            pygame.image.load("assets/composite/sf1_bga_neb2.png").convert(),
            blit_flags=pygame.BLEND_RGBA_ADD,
            parallax_distance=40),
            # lambda: Image(
            # pygame.image.load("assets/composite/sf1_bga_near.png").convert_alpha(),
            # parallax_distance=1)
            )

        self.add_render_plain(self.bg)

    def update(self):
        Engine.update(self)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.bg.viewport.left -= 20
        if keys[pygame.K_RIGHT]:
            self.bg.viewport.left += 20
        if keys[pygame.K_UP]:
            self.bg.viewport.top -= 20
        if keys[pygame.K_DOWN]:
            self.bg.viewport.top += 20

        print(self.fps)


# Keep this minimal.
if __name__ == "__main__":
    pygame.init()
    game = ScrollingBgDemo(pygame.display.set_mode((1024, 512), 0, 32),
                       non_static_background=True, target_fps=120)

    game.start()