"""Typography handler and other classes.
"""
from pprint import pprint

import functools

import pygame


__all__ = ('REGULAR',
           'BOLD',
           'ITALIC',
           'ANTIALIAS',
           'UNDERLINE',
           'FontHandler',
           'render')


REGULAR = 0
BOLD = 1
ITALIC = 2
ANTIALIAS = 4
UNDERLINE = 8


class FontHandler:
    """Font asset and rendering handler.
    """

    # :class:`pygame.font.match_font` permutations.
    _pfm = {REGULAR: pygame.font.match_font,
            BOLD: functools.partial(pygame.font.match_font, bold=True),
            ITALIC: functools.partial(pygame.font.match_font, italic=True),
            BOLD | ITALIC: functools.partial(pygame.font.match_font, bold=True,
                                             italic=True)}

    def __init__(self, parse_fonts={}, fonts={}, load_defaults=True):
        default = {
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

        if load_defaults:
            default.update(parse_fonts)
            parse_fonts = default

        self.__fonts_filepath = FontHandler._parse_fonts_files(parse_fonts)
        self.__fonts_filepath['_debug'] = FontHandler._find_first(
                                                             'courier_new',
                                                             'lucida_console',
                                                             'console',
                                                             'terminal',
                                                             'system')

        self.__cull_fonts_filepath()
        self.__fonts = {}

    @staticmethod
    def _selective_pfm(*args, pfm=None):
        #: Execute the :class:`pygame.font.match_font` function on each
        #: `arg` and return the first one that is an object.
        for arg in args:
            v = pfm(arg or '')
            if v:
                return v

    @staticmethod
    def _parse_fonts_files(font_dict):
        """Parse a dictionary of font names to font files. Uses
        :class:`pygame.font.match_font` to discover a similar font if no
        direct match. Entry is removed if there is no matching font file.

        :param font_dict: Dictionary of fonts to search, value is used in
            priority over the key, but this is rarely needed.
        :rtype dict:
        :return: Dictionary of available font names as keys and font file
            paths as values.
        """

        def __iterate_values():
            for k, v in font_dict.items():
                yield k, {perm_key: FontHandler._selective_pfm(v, k, pfm=pfm)
                            for perm_key, pfm in FontHandler._pfm.items()}

        def __cull_falsy_values():
            for k, v in __iterate_values():
                if any(v.values()):
                    yield k, v

        return dict(__cull_falsy_values())

    @staticmethod
    def _find_first(*names):
        """

        :param names:
        :return:
        """
        for name in names:
            return {perm_key: FontHandler._selective_pfm(name, pfm=pfm)
                        for perm_key, pfm in FontHandler._pfm.items()}

    def __cull_fonts_filepath(self):
        #: This removes any duplicate file entries in a family.
        #: This ensures that pseudo-bold or italic is applied to the
        #: font if that file was already in the family.
        for font_name, family in self.__fonts_filepath.items():
            fam_filepaths = set()
            for n in range(len(family)):
                if family[n] in fam_filepaths:
                    del family[n]
                else:
                    fam_filepaths.add(family[n])

    def __get_filepath(self, name, flags=0):
        if name not in self.__fonts_filepath:
            raise ValueError('Font name: "%s" must be registered with'
                             'the FontHandler. Use `FontHandler.register`' %
                             name)
        try:
            return self.__fonts_filepath[name][flags]
        except KeyError:
            pass

    def get_font(self, name, size, flags=0):
        """
        Also acts as a cache pre-loader.

        :param str name:
        :param int size:
        :param int flags:

        :rtype :class:`pygame.font.Font`:
        :return: Font with specified flags.
        """
        filepath = self.__get_filepath(name, flags=flags)

        # Regular file path to be pseudo-bold and/or italic later.
        r_filepath = not filepath and self.__fonts_filepath[name][0]

        if not filepath and not r_filepath:
            raise ValueError('Font "%s" {size: %s, flags: %s} '
                             'was not found nor did its family have a '
                             'Regular member to use.' % (name, size, flags))

        filepath = filepath or r_filepath

        key = (filepath, size, flags & (BOLD | ITALIC | UNDERLINE))

        # Do we already have the font in cache?
        if key not in self.__fonts:
            self.__fonts[key] = font = pygame.font.Font(filepath, size)
            # Apply pseudo-bold and/or italic if regular file.
            if r_filepath:
                if flags & BOLD:
                    font.set_bold(True)
                if flags & ITALIC:
                    font.set_italic(True)
            # Apply underline.
            if flags & UNDERLINE:
                font.set_underline(True)

        return self.__fonts[key]

# TODO: Move in to appropriate entity.
def render(fonts, name, size, text, color, flags=0, background=None):
    """Provides low level font rendering, retrieving the font using
    the :class:`FontHandler`

    :param `FontHandler` fonts:
    :param str name:
    :param int size:
    :param str text:
    :param :class:`pygame.Color` color:
    :param int flags:
    :param :class:`pygame.Color` background:

    :rtype :class:`pygame.Surface`:
    :return: Surface of the rendered text.
    """

    font = fonts.get_font(name, size, flags=flags)
    return font.render(text, flags & ANTIALIAS, color,
                       background=background)