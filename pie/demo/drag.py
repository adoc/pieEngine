"""pieEngine - Pygame Engine
"""

import pygame

from pie.entity.background import BackgroundImage
from pie.entity.primitive import Fill
from pie.engine import Engine


class Drag(Engine):
    def __init__(self, *args, **kwa):
        Engine.__init__(self, *args, **kwa)
        boxy = (Fill((200, 200),
                                 fill_color=(255, 0, 0),
                                 center=(512, 256)),
                Fill((200, 200),
                                 fill_color=(0, 255, 0),
                                 center=(712, 312)),
                Fill((200, 200),
                                 fill_color=(0, 0, 255),
                                 center=(312, 312)))

        self.events.bind(pygame.KEYDOWN, self.__ev_keydown)

        self.render_group.add(boxy)
        self.drag_handler.extend(boxy)

    def __ev_keydown(self, event):
        if event.key == pygame.K_q:
            self.stop()


if __name__ == "__main__":
    pygame.init()

    sf = lambda: pygame.display.set_mode((1024, 512),
                                         pygame.RESIZABLE)

    bf = lambda: BackgroundImage(
        pygame.image.load("assets/bg1.png").convert())

    game = Drag(screen_factory=sf, background_factory=bf)
    game2 = Drag(screen_factory=sf, background_factory=bf)

    # Runs two iterations of the game if the key "Q" is used to "Quit"
    if game.start():
        game2.start()