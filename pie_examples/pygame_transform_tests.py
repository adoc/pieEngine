import pygame

from pie.entity import FillSurfaceEntity


if __name__ == "__main__":
    #pygame.init()
    #pygame.display.set_mode((100,100))

    # Operate on some pygame object.
    sprite = pygame.sprite.Sprite()
    sprite.rect = pygame.Rect((0,0), (100,100))
    sprite.image = pygame.Surface(sprite.rect.size)
    assert sprite.image.get_size() == (100,100)
    assert sprite.rect.size == (100, 100)

    sprite.image = pygame.transform.scale(sprite.image, (200,200))
    sprite.rect = sprite.image.get_rect()
    assert sprite.image.get_size() == (200,200)
    assert sprite.rect.size == (200,200)

    # Same operations on ``pie.entities``.
    f = FillSurfaceEntity(surface_factory=lambda: pygame.Surface((100, 100)))
    assert f.image.get_size() == (100,100)
    assert f.rect.size == (100, 100)

    f.surface_transform(pygame.transform.scale, (200,200))
    assert f.image.get_size() == (200,200)
    assert f.rect.size == (200,200)