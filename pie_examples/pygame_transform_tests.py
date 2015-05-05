import pygame


if __name__ == "__main__":
    #pygame.init()
    #pygame.display.set_mode((100,100))

    sprite = pygame.sprite.Sprite()
    sprite.rect = pygame.Rect((0,0), (100,100))
    sprite.image = pygame.Surface(sprite.rect.size)

    sprite.image = pygame.transform.scale(sprite.image, (200,200))

    print(sprite.rect)
    print(sprite.image.get_size())