import pygame

from pie.animation import AnimationLoop


class ClickPointSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=1):
        self.rect = pygame.Rect((x, y), (1,1))
        self.radius = radius


class AnimatedSpriteCluster:
    def __init__(self, animated_sprites, pos, size, distribution_function=None, animation_function=None):
        self.__animated_sprites = animated_sprites
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

        self.__distribution_function = distribution_function
        self.__animation_function = animation_function

    def update(self):
        map(lambda s: s.update(), self.__animated_sprites)

    def draw(self, surface):
        map(lambda s: s.draw(surface), self.__animated_sprites)


class DragableSpriteMixin:
    """ Allows a sprite to be dragged.
    Game class must implement ``engine.events.Draghandler``.
    """
    def __init__(self):
        self.__dragging = False
        self.__drag_sprite = ClickPointSprite(0, 0)

    @property
    def dragging(self):
        return self.__dragging

    @property
    def drag_sprite(self):
        return self.__drag_sprite

    def un_drag(self):
        self.__dragging = False
        self.__drag_sprite = ClickPointSprite(*self.rect.center)

    def drag(self, drag_sprite):
        self.__dragging = True
        self.__drag_sprite = drag_sprite