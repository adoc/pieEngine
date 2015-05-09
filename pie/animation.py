"""
"""
from pie.base import MRunnable


class Animation(MRunnable):
    pass


class AnimationLoop(Animation):
    def __init__(self, bounce=False, once=False, auto_start=False):
        MRunnable.__init__(self, auto_start=auto_start)
        self.__bounce = bounce
        self.__once = once

    def update(self, entity):
        if self.running:
            try:
                return
            finally:
                entity.advance()

                if self.__once and entity.at_start:
                    self.__start = False

                if self.__bounce:
                    if entity.at_end:
                        entity.reverse()
                    if entity.at_start and entity.is_reversed:
                        entity.forward()