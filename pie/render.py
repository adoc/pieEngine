"""
"""

import pygame

__all__ = ()


class Renderer:
    """Renderer base class.
    """
    def __init__(self, screen, group):
        pass





class Renderer:
    """
    """
    def __init__(self, screen, background, group,
                 static_background=True):
        self.__screen = screen

        self.__background = background # How do we handle backgrounds?? [#3]
        self.__group = group # Does this stay a group of sprites only? [#3]
        # Do we add the "list of groups" abstract here? [#3]

        if static_background:
            self.render = self.__render_static
            self.clear = self.__clear_static
        else:
            self.render = self.__render_non_static
            self.clear = self.__clear_non_static

    def __clear_static(self):
        self.__group.clear(self.__screen, self.__background.group_clear)

    def __clear_non_static(self):
        self.__screen.blit(self.__background.image, self.__background.rect)

    def __render_static(self):
        pygame.display.update(self.__group.draw(self.__screen))

    def __render_non_static(self):
        self.__group.draw(self.__screen)
        pygame.display.flip()

    def init(self, offset=None):
        # if offset:
        #     self.__background.move_ip(*offset)
        #     for sprite in self.__group:
        #         sprite.move_ip(*offset)

        self.__clear_non_static()
        self.__render_non_static()
        pygame.display.flip()