import unittest

from pie.base import MRunnable


class TestMRunnable(unittest.TestCase):
    def test__init__(self):
        #no arg
        mr = MRunnable()
        self.assertFalse(mr.running)

        mr = MRunnable(auto_start=False)
        self.assertFalse(mr.running)

        mr = MRunnable(auto_start=True)
        self.assertTrue(mr.running)

    def test_start(self):
        mr = MRunnable()
        mr.start()
        self.assertTrue(mr.running)

    def test_stop(self):
        mr = MRunnable(auto_start=True)
        mr.stop()
        self.assertFalse(mr.running)

    def test_running(self):
        mr = MRunnable(auto_start=True)
        self.assertTrue(mr.running)

    def test_stopped(self):
        mr = MRunnable(auto_start=False)
        self.assertTrue(mr.stopped)
