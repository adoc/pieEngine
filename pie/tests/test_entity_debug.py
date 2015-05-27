import unittest


from pie.entity.debug import DebugText



class TestDebugText(unittest.TestCase):
    def test___init__(self):
        dt = DebugText()
        self.assertTrue(hasattr(dt, 'rect'))
        self.assertEqual(dt.rect.topleft, (0, 0))

