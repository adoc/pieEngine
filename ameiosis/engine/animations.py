class AnimationLoop:
    def __init__(self, bounce=True, once=False):
        self.__start = False
        self.__bounce = bounce
        self.__once = once

    def start(self):
        self.__start = True

    def stop(self):
        self.__start = False

    def update(self, sprite):
        if self.__start:
            try:
                return
            finally:
                sprite._frame_index += sprite._frame_interval
                sprite._frame_index %= sprite._frame_count

                if self.__once and sprite._frame_index == 0:
                    self.__start = False

                if self.__bounce:
                    if (sprite._frame_index == sprite._frame_count - 1):
                        sprite._frame_interval = -1
                    if (sprite._frame_index == 0 and sprite._frame_interval < 0):
                        sprite._frame_interval = 1