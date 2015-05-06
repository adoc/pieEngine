import unittest

from pie.engine import Engine

class TestEngineInit(unittest.TestCase):
    def test_init_privates(self):
        assert False

    def test_bound_events(self):
        assert False

class TestEngineEvents(unittest.TestCase):
    def test__ev_resize(self):
        assert False


class TestEngineProperties(unittest.TestCase):
    def test_stopped(self):
        assert False

    def test_screen_width(self):
        assert False

    def test_screen_height(self):
        assert False

    def test_drag_handler(self):
        assert False

    def test_draw_surface(self):
        assert False


class TestEngineMethods(unittest.TestCase):
    def test_append_blit(self):
        assert False

    def test_update(self):
        assert False

    def test_buffer(self):
        assert False

    # TODO: being renamed.
    def test_draw(self):
        assert False

    def test_render(self):
        assert False

    def test_stop(self):
        assert False