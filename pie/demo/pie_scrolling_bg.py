import pygame

from pie.engine import Engine
from pie.entity.primitive import Image
from pie.entity.background import RepeatingImage

class ScrollingBgDemo(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)

        self.bg = RepeatingImage(
            Image(
                pygame.image.load("assets/composite/sf1_bg_near.png").convert(),
                parallax_distance=5),
        )

        # self.bg = RepeatingEntity(
        #     lambda: Image(
        #         pygame.image.load("assets/bg1.png").convert(),
        #         parallax_distance=5))

        self.add_render_plain(self.bg)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.bg.viewport.left -= 33
        if keys[pygame.K_RIGHT]:
            self.bg.viewport.left += 33
        if keys[pygame.K_UP]:
            self.bg.viewport.top -= 33
        if keys[pygame.K_DOWN]:
            self.bg.viewport.top += 33

        Engine.update(self)


# Keep this minimal.
if __name__ == "__main__":
    pygame.init()
    game = ScrollingBgDemo(pygame.display.set_mode((1024, 512), 0, 32),
                       non_static_background=True)

    game.start()