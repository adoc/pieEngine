import unittest
import uuid
from random import SystemRandom

from pie.entity.primitive import Fill


random = SystemRandom()

import pygame

import pie.math
import pie.entity


class TestModuleFuncs(unittest.TestCase):
    """
    """

    def setUp(self):
        pie.entity._reset_entity_ord(confirm=True)

    def test_next_entity_ord(self):
        for i in range(1, 100):
            self.assertEqual(pie.entity.next_entity_ord(), i)

    def test__reset_entity_ord(self):
        for i in range(1, 100):
            self.assertEqual(pie.entity.next_entity_ord(), i)

        pie.entity._reset_entity_ord()
        self.assertEqual(pie.entity.next_entity_ord(), 100)

        pie.entity._reset_entity_ord(confirm=False)
        self.assertEqual(pie.entity.next_entity_ord(), 101)

        pie.entity._reset_entity_ord(confirm=True)
        self.assertEqual(pie.entity.next_entity_ord(), 1)

class TestMIdentity(unittest.TestCase):
    def setUp(self):
        self.__ord = 0
        self.__id = 0
        pie.entity._reset_entity_ord(confirm=True)

    def ord_factory(self):
        self.__ord += 1
        return self.__ord

    def id_factory(self):
        self.__id += 10
        return self.__id

    def test_base_entity(self):
        for i in range(1, 100):
            entity = pie.entity.MIdentity()
            self.assertEqual(entity.ord, i+i-1)
            self.assertIsInstance(entity.id, uuid.UUID)

            entity = pie.entity.MIdentity(ord_factory=self.ord_factory)
            self.assertEqual(entity.ord, self.__ord)

            entity = pie.entity.MIdentity(id_factory=self.id_factory)
            self.assertEqual(entity.id, self.__id)

            entity = pie.entity.MIdentity(ord_factory=self.ord_factory,
                                id_factory=self.id_factory)
            self.assertEqual(entity.ord, self.__ord)
            self.assertEqual(entity.id, self.__id)

    def test_update(self):
        entity = pie.entity.MIdentity()
        self.assertRaises(NotImplementedError, entity.update)

    def test_present(self):
        entity = pie.entity.MIdentity()
        self.assertRaises(NotImplementedError, entity.present)


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


class TestMRect(TestRectBase):
    def test_init_ip(self):
        for pr in self.proto_rect:
            # no init arg.
            self.assertRaises(TypeError, pie.entity.MRect)

            # single init arg (Rect)
            r1 = pie.entity.MRect(pr)
            self.assertIsInstance(r1.rect, pygame.Rect)
            self.assertIsNot(r1.rect, pr)
            self.assertEqual(r1.rect, pr)

            # two init args (topleft), (size)
            r2 = pie.entity.MRect(pr.topleft,
                            pr.size)
            self.assertIsInstance(r2.rect, pygame.Rect)
            self.assertIsNot(r2.rect, pr)
            self.assertEqual(r2.rect, pr)

            # two bad init args
            self.assertRaises(TypeError,
                              lambda: pie.entity.MRect(pr.left,
                                                pr.top))
            
            # three init args
            self.assertRaises(TypeError,
                              lambda: pie.entity.MRect(*pr.topleft + (pr.width,)))

            # four init args
            r3 = pie.entity.MRect(pr.left, pr.top, pr.width, pr.height)
            self.assertIsInstance(r3.rect, pygame.Rect)
            self.assertIsNot(r3.rect, pr)
            self.assertEqual(r3.rect, pr)

            # rect_factory
            r4 = pie.entity.MRect(rect_factory=self._rect_factory)
            self.assertIsInstance(r4.rect, pygame.Rect)
            self.assertGreaterEqual(r4.rect.top, 0)
            self.assertLessEqual(r4.rect.top, 1000)
            self.assertGreaterEqual(r4.rect.bottom, 0)
            self.assertLessEqual(r4.rect.bottom, 2000)
            self.assertGreaterEqual(r4.rect.bottom, r4.rect.top)

    def test_move_ip(self):
        for pr in self.proto_rect:
            r = pie.entity.MRect(rect_factory=self._rect_factory)
            or_topleft = r.rect.topleft
            or_bottomright = r.rect.bottomright
            offset = pr.topleft # Not related to the actual topleft.
            r.move_ip(*offset)
            self.assertEqual(r.rect.topleft, pie.math.vect_sum(or_topleft,
                                                          offset))
            self.assertEqual(r.rect.bottomright, pie.math.vect_sum(or_bottomright,
                                                          offset))

    def test_inflate_ip(self):
        for pr in self.proto_rect:
            r = pie.entity.MRect(rect_factory=self._rect_factory)
            o_r = r.rect.copy()
            offset = pr.topleft # Not related to the actual topleft.
            r.inflate_ip(*offset)
            self.assertEqual(r.rect.width, o_r.width + offset[0])
            self.assertEqual(r.rect.height, o_r.height + offset[1])
            self.assertAlmostEqual(r.rect.center[0], o_r.center[0], delta=1)
            self.assertAlmostEqual(r.rect.center[1], o_r.center[1], delta=1)

    def test_clamp_ip(self):
        assert False

    def test_clip_ip(self):
        assert False

    def test_union_ip(self):
        assert False

    def test_unionall_ip(self):
        assert False

    def test_fit_ip(self):
        assert False


class TestSurfaceEntity(TestRectBase):
    def test_init(self):
        for pr in self.proto_rect:
            # no arg.
            self.assertRaises(TypeError, pie.entity.MSurface)

            # one arg
            s = pie.entity.MSurface(pr.size)
            self.assertEqual(s.surface.get_size(), pr.size)

            # two args
            s = pie.entity.MSurface(pr.size, 0)
            self.assertEqual(s.surface.get_flags(), 0)
            s = pie.entity.MSurface(pr.size, pygame.SRCALPHA)
            self.assertEqual(s.surface.get_flags(), pygame.SRCALPHA)

            # three args
            s = pie.entity.MSurface(pr.size, 0, 8)
            self.assertEqual(s.surface.get_bitsize(), 8)
            s = pie.entity.MSurface(pr.size, 0, 16)
            self.assertEqual(s.surface.get_bitsize(), 16)
            s = pie.entity.MSurface(pr.size, 0, 24)
            self.assertEqual(s.surface.get_bitsize(), 24)
            s = pie.entity.MSurface(pr.size, 0, 32)
            self.assertEqual(s.surface.get_bitsize(), 32)

            # surface factory
            s = pie.entity.MSurface(surface_factory=
                              lambda: pygame.Surface(pr.size))
            self.assertEqual(s.surface.get_size(), pr.size)


    def test_surface_convert(self):
        # TODO: Possibly incomplete test coverage
        pygame.init()
        for pr in self.proto_rect:
            so = pygame.Surface(pr.size, 0, 8)

            s1 = pie.entity.MSurfaceRect(pr.size, pygame.HWSURFACE, 32)
            s1.convert_ip(so)

            self.assertEqual(s1.surface.get_flags(), 0)
            self.assertEqual(s1.surface.get_bitsize(), 8)

    def test_surface_convert_alpha(self):
        # TODO: Possibly incomplete test coverage
        pygame.init()
        pygame.display.set_mode((100,100), pygame.SRCALPHA, 32)
        for pr in self.proto_rect:
            so = pygame.Surface(pr.size, pygame.SRCALPHA, 32)

            s1 = pie.entity.MSurfaceRect(pr.size, 0, 24)
            s1.convert_alpha_ip(so)

            self.assertEqual(s1.surface.get_flags(), pygame.SRCALPHA)
            self.assertEqual(s1.surface.get_bitsize(), 32)


class TestSurfaceRectEntity(TestRectBase):
    def test_init(self):
        for pr in self.proto_rect:
            pr_r = self.proto_rect[self.frndi(len(self.proto_rect))]
            # no arg.
            self.assertRaises(TypeError, pie.entity.MSurfaceRect)

            # one arg
            s = pie.entity.MSurfaceRect(pr.size)
            self.assertEqual(s.surface.get_size(), pr.size)
            self.assertIsNot(s.rect, pr)
            self.assertEqual(s.rect.size, pr.size)

            # one arg (rect_kwa)
            s = pie.entity.MSurfaceRect(pr.size, center=pr.center)
            self.assertEqual(s.surface.get_size(), pr.size)
            self.assertIsNot(s.rect, pr)
            self.assertEqual(s.rect, pr)

            s = pie.entity.MSurfaceRect(pr.size, topleft=pr.topleft)
            self.assertEqual(s.surface.get_size(), pr.size)
            self.assertIsNot(s.rect, pr)
            self.assertEqual(s.rect, pr)

            # two args
            s = pie.entity.MSurfaceRect(pr.size, 0)
            self.assertEqual(s.surface.get_flags(), 0)
            s = pie.entity.MSurfaceRect(pr.size, pygame.SRCALPHA)
            self.assertEqual(s.surface.get_flags(), pygame.SRCALPHA)
            
            # three args
            s = pie.entity.MSurfaceRect(pr_r.size, 0, 8)
            self.assertEqual(s.surface.get_bitsize(), 8)
            s = pie.entity.MSurfaceRect(pr_r.size, 0, 16)
            self.assertEqual(s.surface.get_bitsize(), 16)
            s = pie.entity.MSurfaceRect(pr_r.size, 0, 24)
            self.assertEqual(s.surface.get_bitsize(), 24)
            s = pie.entity.MSurfaceRect(pr_r.size, 0, 32)
            self.assertEqual(s.surface.get_bitsize(), 32)

            # surface factory
            s = pie.entity.MSurfaceRect(surface_factory=
                                    lambda: pygame.Surface(pr.size),
                                  center=pr.center)
            self.assertEqual(s.surface.get_size(), pr.size)
            self.assertIsNot(s.rect, pr)
            self.assertEqual(s.rect, pr)

    def test_rect_inflate(self):
        assert False

    def test_rect_clamp(self):
        assert False

    def test_rect_clip(self):
        assert False

    def test_rect_union(self):
        assert False

    def test_rect_unionall(self):
        assert False

    def test_rect_fit(self):
        assert False


class TestPointEntity(unittest.TestCase):
    def test__init__(self):
        assert False


class TestSpriteEntity(unittest.TestCase):
    def test_init(self):
        assert False


class TestDirtySpriteEntity(unittest.TestCase):
    def test_init(self):
        assert False


class TestDrawSurfaceEntity(unittest.TestCase):
    def test_init(self):
        assert False


class TestFill(TestRectBase):
    def test_init(self):
        pass

    def test_update(self):
        s = Fill((100,100), 0, 24)
        for byte in s.surface.get_buffer().raw:
            self.assertEqual(byte, 0)

        s = Fill((100,100), 0, 24, fill_color=(255,255,255))
        for byte in s.surface.get_buffer().raw:
            self.assertEqual(byte, 255)


class TestMAnimated(unittest.TestCase):
    def test_init_and_props(self):
        # Test "regular args.
        a = pie.entity.MAnimated()

        self.assertEqual(a.start, 0)
        self.assertEqual(a.end, -1)
        self.assertEqual(a.count, 0)
        self.assertEqual(a.playing_count, 0)
        self.assertEqual(a.interval, 1)
        self.assertEqual(a.index, 0)
        self.assertTrue(a.at_start)
        self.assertTrue(a.at_end)
        self.assertFalse(a.is_reversed)
        self.assertTrue(a.is_forward)

        a = pie.entity.MAnimated(count=60)

        self.assertEqual(a.start, 0)
        self.assertEqual(a.end, 59)
        self.assertEqual(a.count, 60)
        self.assertEqual(a.playing_count, 60)
        self.assertEqual(a.interval, 1)
        self.assertEqual(a.index, 0)
        self.assertTrue(a.at_start)
        self.assertFalse(a.at_end)
        self.assertFalse(a.is_reversed)
        self.assertTrue(a.is_forward)

        a = pie.entity.MAnimated(count=60, interval=-1)

        self.assertEqual(a.start, 0)
        self.assertEqual(a.end, 59)
        self.assertEqual(a.count, 60)
        self.assertEqual(a.playing_count, 60)
        self.assertEqual(a.interval, -1)
        self.assertEqual(a.index, 0)
        self.assertTrue(a.at_start)
        self.assertFalse(a.at_end)
        self.assertTrue(a.is_reversed)
        self.assertFalse(a.is_forward)

        a = pie.entity.MAnimated(count=60, interval=-1,
                                 start=10)

        self.assertEqual(a.start, 10)
        self.assertEqual(a.end, 59)
        self.assertEqual(a.count, 60)
        self.assertEqual(a.playing_count, 50)
        self.assertEqual(a.interval, -1)
        self.assertEqual(a.index, 10)
        self.assertTrue(a.at_start)
        self.assertFalse(a.at_end)
        self.assertTrue(a.is_reversed)
        self.assertFalse(a.is_forward)

        a = pie.entity.MAnimated(count=60, interval=-1,
                                 start=10, end=20)

        self.assertEqual(a.start, 10)
        self.assertEqual(a.end, 20)
        self.assertEqual(a.count, 60)
        self.assertEqual(a.playing_count, 11)
        self.assertEqual(a.interval, -1)
        self.assertEqual(a.index, 10)
        self.assertTrue(a.at_start)
        self.assertFalse(a.at_end)
        self.assertTrue(a.is_reversed)
        self.assertFalse(a.is_forward)

        # Test irregular args.
        a = pie.entity.MAnimated(count=60, interval=-1,
                                 start=20, end=10)

        self.assertEqual(a.start, 20)
        self.assertEqual(a.end, 10)
        self.assertEqual(a.count, 60)
        # Weird result
        self.assertEqual(a.playing_count, 9)
        self.assertEqual(a.interval, -1)
        self.assertEqual(a.index, 20)
        self.assertTrue(a.at_start)
        # Another funky result
        self.assertTrue(a.at_end)
        self.assertTrue(a.is_reversed)
        self.assertFalse(a.is_forward)

    def test_prop_at_start(self):
        assert False

    def test_prop_at_end(self):
        assert False

    def test_prop_is_reversed(self):
        assert False

    def test_prop_surface(self):
        assert False

    def test_advance(self):
        assert False

    def test_negate_interval(self):
        assert False

    def test_rewind(self):
        assert False

    def test_update(self):
        assert False

    def test_present(self):
        assert False

