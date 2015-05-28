"""Typography handler and other classes.
"""

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


class Font:
    """
    Primarily a wrapper for :class:`pygame.font.Font` that exposes
    most of the API, though slightly different.
    """
    def __init__(self, font, flags=0, pseudo=False):
        self.__font = font
        self.__flags = flags
        self.__pseudo = pseudo

        if pseudo:
            if flags & BOLD:
                font.set_bold(True)
            if flags & ITALIC:
                font.set_italic(True)
        if flags & UNDERLINE:
            font.set_underline(True)

    @property
    def is_pseudo(self):
        return self.__pseudo is True

    @property
    def linesize(self):
        return self.__font_get_linesize()

    @property
    def height(self):
        return self.__font.get_height()

    @property
    def ascent(self):
        return self.__font.get_ascent()

    @property
    def descent(self):
        return self.__font.get_descent()

    def metrics(self, text):
        pass

    def size(self, text):
        pass

    def render(self, text, color, background=None):
        """Provides low level font rendering, retrieving the font using
        the :class:`FontHandler`

        :param str text:
        :param :class:`pygame.Color` color:
        :param int flags:
        :param :class:`pygame.Color` background:

        :rtype :class:`pygame.Surface`:
        :return: Surface of the rendered text.
        """

        return self.__font.render(text, self.__flags & ANTIALIAS, color,
                                  background)

class FontHandler:
    """Font asset and rendering handler.
    """

    # :class:`pygame.font.match_font` permutations.
    _pfm = {REGULAR: pygame.font.match_font,
            BOLD: functools.partial(pygame.font.match_font, bold=True),
            ITALIC: functools.partial(pygame.font.match_font, italic=True),
            BOLD | ITALIC: functools.partial(pygame.font.match_font, bold=True,
                                             italic=True)}

    def __init__(self, parse_fonts={}, fonts={}, load_defaults=True,
                 default_flags=0):
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

        self.__default_flags = default_flags

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

    def get_font(self, name, size, flags=0):
        """
        Also acts as a cache pre-loader.

        :param str name:
        :param int size:
        :param int flags:

        :rtype :class:`pygame.font.Font`:
        :return: Font with specified flags.
        """

        flags = self.__default_flags | flags

        if name not in self.__fonts_filepath:
            raise ValueError('Font "%s" is not registered with the '
                             'FontHandler. Use `FontHandler.register` to do '
                             'so' % name)
        try:
            filepath =  self.__fonts_filepath[name][flags &
                                                    (REGULAR | BOLD | ITALIC)]
            # Restrict the flags to the ones that determine the file.
        except KeyError:
            filepath = self.__fonts_filepath[name][0]
            # Due to previous `if` can only be KeyError on `flags`.

            if not filepath:
                raise ValueError('Font "%s" {size: %s, flags: %s} was not '
                                 'found nor did its family have a Regular '
                                 'member to use.' % (name, size, flags))

            pseudo=True
        else:
            pseudo = False

        key = (filepath, size, flags)

        # Do we already have the font in cache?
        if key not in self.__fonts:
            self.__fonts[key] = Font(pygame.font.Font(filepath, size),
                                     flags=flags, pseudo=pseudo)

        return self.__fonts[key]