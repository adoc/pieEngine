import unittest

import pygame

from pie.entity.animated import SurfaceSequence
from pie.animation import AnimationLoop
from pie import MRunnable


class TestAnimation(unittest.TestCase):
    def test_init(self):
        a = MRunnable()
        self.assertFalse(a._Animation__running)

        a = MRunnable(auto_start=True)
        self.assertTrue(a._Animation__running)

    def test_start(self):
        a = MRunnable()
        a.start()
        self.assertTrue(a._Animation__running)

    def test_stop(self):
        a = MRunnable()
        a.stop()
        self.assertFalse(a._Animation__running)

    def test_running(self):
        a = MRunnable()
        a.start()
        self.assertTrue(a.running)

    def test_stopped(self):
        a = MRunnable()
        a.start()
        self.assertFalse(a.stopped)


class TestAnimationLoop(unittest.TestCase):
    def test_init(self):
        a = AnimationLoop(None)
        self.assertIsNone(a._AnimationLoop__ae)
        self.assertTrue(a._AnimationLoop__bounce)
        self.assertFalse(a._AnimationLoop__once)
        self.assertFalse(a.running)

        a = AnimationLoop(None, bounce=False, once=True, auto_start=True)
        self.assertIsNone(a._AnimationLoop__ae)
        self.assertFalse(a._AnimationLoop__bounce)
        self.assertTrue(a._AnimationLoop__once)
        self.assertTrue(a.running)

    def test_update(self):
        frames = [pygame.Surface((100,100))] * 30
        ae = SurfaceSequence(frames, autostart=False,
                            animation_cls=AnimationLoop)

        a = AnimationLoop(ae)
        a.start()
        a.update()

