import pygame


if __name__ == "__main__":
    pygame.init()

    # print(pygame.display.get_wm_info())
    # print(pygame.display.list_modes())

    info = pygame.display.Info()
    print(info)
    print(info.current_w)