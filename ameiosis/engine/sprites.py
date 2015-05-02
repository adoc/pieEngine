import pygame

from ameiosis.engine import AnimationLoop, ClickPointSprite


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, frames, pos, size, autostart=True,
                 animation_obj=AnimationLoop()):
        pygame.sprite.Sprite.__init__(self)
        self.__frames = tuple(frames) # Not mutable for now.
        self._frame_index = 0
        self._frame_interval = 1
        self._frame_count = len(frames)
        self.__animation_obj = animation_obj
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        if autostart:
            self.__animation_obj.start()

    @property
    def frame(self):
        return self.__frames[self._frame_index]

    def reset(self):
        self._frame_index = 0

    def draw(self, surface):
       surface.blit(self.frame, self.rect.topleft)

    def update(self):
        self.__animation_obj.update(self)


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
    def __init__(self, *args, **kwa):
        self.__dragging = False
        self.__drag_sprite = ClickPointSprite(0, 0)

    @property
    def dragging(self):
        return self.__dragging

    def un_drag(self):
        self.__dragging = False
        self.__drag_sprite = ClickPointSprite(*self.rect.center)

    def drag(self, drag_sprite):
        self.__dragging = True
        self.__drag_sprite = drag_sprite