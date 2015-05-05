import unittest
import uuid
from random import SystemRandom
random = SystemRandom()

import pygame

from ameiosis.engine import entities
from ameiosis.engine.entities import (next_entity_ord, BaseEntity, RectEntity,
                                      SurfaceEntity, SurfaceRectEntity,
                                      FillSurfaceEntity)


class TestModuleFuncs(unittest.TestCase):
    """
    """

    def setUp(self):
        entities._reset_entity_ord(confirm=True)

    def test_next_entity_ord(self):
        for i in range(1, 100):
            self.assertEqual(next_entity_ord(), i)

    def test_entity_base(self):
        for i in range(1, 100):
            entity = BaseEntity()
            self.assertEqual(entity.ord, i)
            self.assertIsInstance(entity.uuid, uuid.UUID)
            self.assertIsInstance(entity.id, int)
            self.assertGreater(entity.id, 0 )


class TestRectBase(unittest.TestCase):
    @staticmethod
    def frndi(f, off=0):
        return int(random.random() * f + off)

    def _rect_factory(self):
         return pygame.Rect(self.frndi(1000), self.frndi(1000),
                            self.frndi(1000)+1,
                            self.frndi(1000)+1)

    def setUp(self):
        self.proto_rect = []
        for _ in range(10):
            self.proto_rect.append(self._rect_factory())


class TestRectEntity(TestRectBase):
    def test_init(self):
        for pr in self.proto_rect:
            # no init arg.
            self.assertRaises(TypeError, RectEntity)

            # single init arg (Rect)
            r1 = RectEntity(pr)
            self.assertIsInstance(r1.rect, pygame.Rect)
            self.assertIsNot(r1.rect, pr)
            self.assertEqual(r1.rect, pr)

            # two init args (topleft), (size)
            r2 = RectEntity(pr.topleft,
                            pr.size)
            self.assertIsInstance(r2.rect, pygame.Rect)
            self.assertIsNot(r2.rect, pr)
            self.assertEqual(r2.rect, pr)

            # two bad init args
            self.assertRaises(TypeError,
                              lambda: RectEntity(pr.left,
                                                pr.top))
            
            # three init args
            self.assertRaises(TypeError,
                              lambda: RectEntity(*pr.topleft + (pr.width,)))

            # four init args
            r3 = RectEntity(pr.left, pr.top, pr.width, pr.height)
            self.assertIsInstance(r3.rect, pygame.Rect)
            self.assertIsNot(r3.rect, pr)
            self.assertEqual(r3.rect, pr)

            # rect_factory
            r4 = RectEntity(rect_factory=self._rect_factory)
            self.assertIsInstance(r4.rect, pygame.Rect)
            self.assertGreaterEqual(r4.rect.top, 0)
            self.assertLessEqual(r4.rect.top, 1000)
            self.assertGreaterEqual(r4.rect.bottom, 0)
            self.assertLessEqual(r4.rect.bottom, 2000)
            self.assertGreaterEqual(r4.rect.bottom, r4.rect.top)


    def test_rect_reset(self):
        for pr in self.proto_rect:
            pr_r = self.proto_rect[self.frndi(len(self.proto_rect))]

            r1 = RectEntity(pr)
            self.assertIsInstance(r1.rect, pygame.Rect)
            self.assertIsNot(r1.rect, pr)
            self.assertEqual(r1.rect, pr)

            # no arg.
            self.assertRaises(TypeError, r1.reset)

            # single arg (Rect)
            r1.reset(pr_r)
            self.assertIsInstance(r1.rect, pygame.Rect)
            self.assertIsNot(r1.rect, pr_r)
            self.assertEqual(r1.rect, pr_r)

            # two args (topleft), (size)
            r1.reset(pr.topleft,
                          pr.size)
            self.assertIsInstance(r1.rect, pygame.Rect)
            self.assertIsNot(r1.rect, pr)
            self.assertEqual(r1.rect, pr)

            # two bad args
            self.assertRaises(TypeError,
                              lambda: r1.reset(pr.left,
                                                    pr.top))

            # three bad args
            self.assertRaises(TypeError,
                              lambda: r1.reset(*pr.topleft + (pr.width,)))
            
            # four args
            r1.reset(pr_r.left, pr_r.top, pr_r.width, pr_r.height)
            self.assertIsInstance(r1.rect, pygame.Rect)
            self.assertIsNot(r1.rect, pr_r)
            self.assertEqual(r1.rect, pr_r)

            # rect_factory
            r1.reset(rect_factory=self._rect_factory)
            self.assertIsInstance(r1.rect, pygame.Rect)
            self.assertGreaterEqual(r1.rect.top, 0)
            self.assertLessEqual(r1.rect.top, 1000)
            self.assertGreaterEqual(r1.rect.bottom, 0)
            self.assertLessEqual(r1.rect.bottom, 2000)
            self.assertGreaterEqual(r1.rect.bottom, r1.rect.top)


class TestSurfaceEntity(TestRectBase):
    def test_init(self):
        for pr in self.proto_rect:
            # no arg.
            self.assertRaises(TypeError, SurfaceEntity)

            # one arg
            s = SurfaceEntity(pr.size)
            self.assertEqual(s.surface.get_size(), pr.size)

            # two args
            s = SurfaceEntity(pr.size, 0)
            self.assertEqual(s.surface.get_flags(), 0)
            s = SurfaceEntity(pr.size, pygame.SRCALPHA)
            self.assertEqual(s.surface.get_flags(), pygame.SRCALPHA)

            # three args
            s = SurfaceEntity(pr.size, 0, 8)
            self.assertEqual(s.surface.get_bitsize(), 8)
            s = SurfaceEntity(pr.size, 0, 16)
            self.assertEqual(s.surface.get_bitsize(), 16)
            s = SurfaceEntity(pr.size, 0, 24)
            self.assertEqual(s.surface.get_bitsize(), 24)
            s = SurfaceEntity(pr.size, 0, 32)
            self.assertEqual(s.surface.get_bitsize(), 32)

            # surface factory
            s = SurfaceEntity(surface_factory=
                              lambda: pygame.Surface(pr.size))
            self.assertEqual(s.surface.get_size(), pr.size)

    def test_surface_reset(self):
        for pr in self.proto_rect:
            pr_r = self.proto_rect[self.frndi(len(self.proto_rect))]

            s = SurfaceEntity(pr.size)

            # no arg.
            self.assertRaises(TypeError, s.reset)

            # one arg
            s.reset(pr_r.size)
            self.assertEqual(s.surface.get_size(), pr_r.size)

            # two args
            s.reset(pr.size, 0)
            self.assertEqual(s.surface.get_flags(), 0)
            s.reset(pr.size, pygame.SRCALPHA)
            self.assertEqual(s.surface.get_flags(), pygame.SRCALPHA)

            # three args
            s.reset(pr_r.size, 0, 8)
            self.assertEqual(s.surface.get_bitsize(), 8)
            s = SurfaceEntity(pr_r.size, 0, 16)
            self.assertEqual(s.surface.get_bitsize(), 16)
            s = SurfaceEntity(pr_r.size, 0, 24)
            self.assertEqual(s.surface.get_bitsize(), 24)
            s = SurfaceEntity(pr_r.size, 0, 32)
            self.assertEqual(s.surface.get_bitsize(), 32)

            # surface factory
            s.reset(surface_factory=
                              lambda: pygame.Surface(pr.size))
            self.assertEqual(s.surface.get_size(), pr.size)

    def test_surface_convert(self):
        # TODO: Possibly incomplete test coverage
        pygame.init()
        for pr in self.proto_rect:
            so = pygame.Surface(pr.size, 0, 8)

            s1 = SurfaceRectEntity(pr.size, pygame.HWSURFACE, 32)
            s1.surface_convert(so)

            self.assertEqual(s1.surface.get_flags(), 0)
            self.assertEqual(s1.surface.get_bitsize(), 8)

    def test_surface_convert_alpha(self):
        # TODO: Possibly incomplete test coverage
        pygame.init()
        pygame.display.set_mode((100,100), pygame.SRCALPHA, 32)
        for pr in self.proto_rect:
            so = pygame.Surface(pr.size, 0, 8)

            s1 = SurfaceRectEntity(pr.size, 0, 24)
            s1.surface_convert_alpha(so)

            self.assertEqual(s1.surface.get_flags(), pygame.SRCALPHA)
            self.assertEqual(s1.surface.get_bitsize(), 32)


class TestSurfaceRectEntity(TestRectBase):
    def test_init(self):
        for pr in self.proto_rect:
            pr_r = self.proto_rect[self.frndi(len(self.proto_rect))]
            # no arg.
            self.assertRaises(TypeError, SurfaceRectEntity)

            # one arg
            s = SurfaceRectEntity(pr.size)
            self.assertEqual(s.surface.get_size(), pr.size)
            self.assertIsNot(s.rect, pr)
            self.assertEqual(s.rect.size, pr.size)

            # one arg (rect_kwa)
            s = SurfaceRectEntity(pr.size, center=pr.center)
            self.assertEqual(s.surface.get_size(), pr.size)
            self.assertIsNot(s.rect, pr)
            self.assertEqual(s.rect, pr)

            s = SurfaceRectEntity(pr.size, topleft=pr.topleft)
            self.assertEqual(s.surface.get_size(), pr.size)
            self.assertIsNot(s.rect, pr)
            self.assertEqual(s.rect, pr)

            # two args
            s = SurfaceRectEntity(pr.size, 0)
            self.assertEqual(s.surface.get_flags(), 0)
            s = SurfaceRectEntity(pr.size, pygame.SRCALPHA)
            self.assertEqual(s.surface.get_flags(), pygame.SRCALPHA)
            
            # three args
            s.reset(pr_r.size, 0, 8)
            self.assertEqual(s.surface.get_bitsize(), 8)
            s = SurfaceRectEntity(pr_r.size, 0, 16)
            self.assertEqual(s.surface.get_bitsize(), 16)
            s = SurfaceRectEntity(pr_r.size, 0, 24)
            self.assertEqual(s.surface.get_bitsize(), 24)
            s = SurfaceRectEntity(pr_r.size, 0, 32)
            self.assertEqual(s.surface.get_bitsize(), 32)

            # surface factory
            s = SurfaceRectEntity(surface_factory=
                                    lambda: pygame.Surface(pr.size),
                                  center=pr.center)
            self.assertEqual(s.surface.get_size(), pr.size)
            self.assertIsNot(s.rect, pr)
            self.assertEqual(s.rect, pr)

    def test_surface_reset(self):
        for pr in self.proto_rect:
            pr_r = self.proto_rect[self.frndi(len(self.proto_rect))]
            # no arg.
            self.assertRaises(TypeError, SurfaceRectEntity)

            # one arg
            s = SurfaceRectEntity(pr.size)
            
            s.reset(pr_r.size)
            self.assertEqual(s.surface.get_size(), pr_r.size)
            self.assertIsNot(s.rect, pr_r)
            self.assertEqual(s.rect.size, pr_r.size)

            # one arg (rect_kwa)
            s.reset(pr.size, center=pr.center)
            self.assertEqual(s.surface.get_size(), pr.size)
            self.assertIsNot(s.rect, pr)
            self.assertEqual(s.rect, pr)

            s.reset(pr_r.size, topleft=pr_r.topleft)
            self.assertEqual(s.surface.get_size(), pr_r.size)
            self.assertIsNot(s.rect, pr_r)
            self.assertEqual(s.rect, pr_r)

            # two args
            s.reset(pr.size, 0)
            self.assertEqual(s.surface.get_flags(), 0)
            s.reset(pr.size, pygame.SRCALPHA)
            self.assertEqual(s.surface.get_flags(), pygame.SRCALPHA)
            
            # three args
            s.reset(pr_r.size, 0, 8)
            self.assertEqual(s.surface.get_bitsize(), 8)
            s.reset(pr_r.size, 0, 16)
            self.assertEqual(s.surface.get_bitsize(), 16)
            s.reset(pr_r.size, 0, 24)
            self.assertEqual(s.surface.get_bitsize(), 24)
            s.reset(pr_r.size, 0, 32)
            self.assertEqual(s.surface.get_bitsize(), 32)

            # surface factory
            s.reset(surface_factory=
                                    lambda: pygame.Surface(pr.size),
                                  center=pr.center)
            self.assertEqual(s.surface.get_size(), pr.size)
            self.assertIsNot(s.rect, pr)
            self.assertEqual(s.rect, pr)

    def test_present(self):
        for pr in self.proto_rect:
            s = SurfaceRectEntity(pr.size, topleft=pr.topleft)
            surface, rect = s.present()
            self.assertIs(surface, s.surface)
            self.assertIs(rect, s.rect)


class TestFillEntity(TestRectBase):
    def test_init(self):
        pass

    def test_update(self):
        s = FillSurfaceEntity((100,100), 0, 24)
        for byte in s.surface.get_buffer().raw:
            self.assertEqual(byte, 0)

        s = FillSurfaceEntity((100,100), 0, 24, fill_color=(255,255,255))
        for byte in s.surface.get_buffer().raw:
            self.assertEqual(byte, 255)