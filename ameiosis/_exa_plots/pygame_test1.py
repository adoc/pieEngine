import pygame
import pygame.time
from pygame.locals import *

from ameiosis.game import CircleSprite, Ameosis


if __name__ == "__main__":
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((1024, 512))
    font = pygame.font.Font(None, 20)

    game = Ameosis(screen, clock)

    while not game.done:
        # Last to blit overlay(s).
        text = font.render("FPS %d" % clock.get_fps(), 1, (240, 240, 240))
        screen.blit(text, (8,8))

        game.buffer()
        game.handle_events()
        game.draw()
        game.draw_debug()