import unittest

import pygame

import pie.typo


class TestModuleFuncs(unittest.TestCase):
    def test_parse_fonts_files(self):
        font_dict = {
                'montserrat':None,
                'helvetica':None,
                'times':None,
                'georgia':None,
                'impact': None,
                'verdana': None,
                'comic_sans': 'Comic Sans MS',
                'courier_new': None,
                'courier': None,
                'console': None,
                'system': None,
                'terminal': None,
                'lucida_console':None
                }

        parsed = pie.typo._parse_fonts_files(font_dict)

        self.assertLessEqual(len(parsed), len(font_dict))

        for k, v in parsed.items():
            self.assertIsInstance(k, str)
            self.assertGreater(len(k), 1)

            self.assertIsInstance(v, tuple)
            self.assertEqual(len(v), 4)


class TestFileHandler(unittest.TestCase):
    def setUp(self):
        pygame.init()

    def test_init__(self):



        self.assertTrue(True)