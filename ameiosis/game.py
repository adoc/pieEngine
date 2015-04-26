import pygame
import pygame.sprite
import pygame.draw


class Blob(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self._size_mult = 10
        self.color = (150,150,150)


    def draw(self, surface, size):
        s_rect = surface.get_rect()
        size = size * self._size_mult
        self.rect = pygame.draw.circle(surface, self.color, (s_rect[-2]//2, s_rect[-1]//2), size)
