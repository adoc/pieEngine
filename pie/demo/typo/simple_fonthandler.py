import pygame

import pie.engine
import pie.entity.primitive
import pie.typo


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    fh = pie.typo.FontHandler(default_flags=pie.typo.ANTIALIAS)
    # Engine
    s = pygame.display.set_mode((1024, 512), 0, 32)
    e = pie.engine.Engine(s)

    d_font = fh.get_font('_debug', 24, flags=pie.typo.UNDERLINE)

    fonts = (fh.get_font('montserrat', 18),
             fh.get_font('montserrat', 18, flags=pie.typo.BOLD),
             fh.get_font('montserrat', 18, flags=pie.typo.ITALIC),
             )

    text1 = "abcdefghijklmnopqrstuvwxyz"
    text2 = text1.upper()

    surfs = []
    white = (240, 240, 240)
    grey = (200, 200, 200)
    for f in fonts:
        col = []
        col.append(f.render(text1, white))
        col.append(f.render(text2, white))

        max_x = 0
        max_y = 0
        for surf in col:
            max_x = max(max_x, surf.get_width())
            max_y += surf.get_height()

        padding = (8, 8)
        col_surf = pygame.Surface((max_x+(padding[0]*2),
                                   max_y+(padding[1]*2))).convert()

        y = 0
        for surf in col:
            col_surf.blit(surf, (padding[0], y+padding[1]))
            y += surf.get_height()

        surfs.append(col_surf)

    x = 8
    for surf in surfs:
        i = pie.entity.primitive.Image(surf, topleft=(x, 0))
        e.add_render_plain(i)
        x += i.surface.get_width()

    e.start()