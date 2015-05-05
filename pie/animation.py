class Animation:
    def __init__(self, auto_start=False):
        self.__running = auto_start

    def start(self):
        self.__running = True

    def stop(self):
        self.__running = False

    @property
    def running(self):
        return self.__running

    @property
    def stopped(self):
        return not self.__running


class AnimationLoop(Animation):
    def __init__(self, animated_entity, bounce=True, once=False, auto_start=False):
        Animation.__init__(self, auto_start=auto_start)
        self.__ae = animated_entity
        self.__bounce = bounce
        self.__once = once

    def update(self):
        if self.running:
            try:
                return
            finally:
                self.__ae.advance()

                if self.__once and self.__ae.at_start:
                    self.__start = False

                if self.__bounce:
                    if self.__ae.at_end:
                        self.__ae.negate_interval()
                    if self.__ae.at_start and self.__ae.is_reversed:
                        self.__ae.negate_interval()