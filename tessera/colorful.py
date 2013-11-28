# -*- coding: utf-8 -*-

import sys

try:
    from colorama import init as init_ansi_colors_on_windows
    init_ansi_colors_on_windows()
except ImportError:
    pass


class Modifiers:
    """ANSI modifiers for Colorful"""
    reset = 0
    bold = 1
    italic = 3
    underline = 4
    blink = 5
    inverse = 7
    strikethrough = 9


class ForeColors:
    """ANSI foreground colors for Colorful"""
    black = 30
    red = 31
    green = 32
    brown = 33
    blue = 34
    magenta = 35
    cyan = 36
    white = 37
    normal = 39


class BackColors:
    """ANSI background colors for Colorful"""
    black = 40
    red = 41
    green = 42
    yellow = 43
    blue = 44
    magenta = 45
    cyan = 46
    white = 47
    normal = 49


class ANSISequenceNotFoundError(Exception):
    """Error if an ANSI sequence could not be found"""
    def __init__(self, modetype, name):
        self._modetype = modetype
        self._name = name

    def __str__(self):
        return "ANSI Sequence `%s` could not be found in `%s`" % (self._name, self._modetype)


class ColorfulParser:
    """Colorful is a class to decorate text with ANSI colors and modifiers."""
    _modifiers = Modifiers()
    _forecolors = ForeColors()
    _backcolors = BackColors()

    _modifier_splitter = "and"
    _backcolor_splitter = "on"

    @classmethod
    def _is_modifier(cls, modifier):
        return hasattr(cls._modifiers, modifier)

    @classmethod
    def _get_ansi_decorator(cls, mode):
        return "\033[%sm" % (mode)

    @classmethod
    def _translate_to_ansi_decorator(cls, modetype, name):
        if hasattr(modetype, name):
            return cls._get_ansi_decorator(getattr(modetype, name))
        else:
            raise ANSISequenceNotFoundError(modetype.__class__.__name__, name)

    @classmethod
    def parse_attr(cls, attr):
        parts = attr.split("_")

        modifiers = ""
        forecolor = ""
        backcolor = ""

        if cls._is_modifier(parts[0]):
            modifiers += cls._translate_to_ansi_decorator(cls._modifiers, parts[0])
            parts = parts[1:]

        if cls._modifier_splitter in parts:
            for part in [parts[p + 1] if p + 1 < len(parts) else None for p in range(len(parts)) if parts[p] == cls._modifier_splitter]:
                modifiers += cls._translate_to_ansi_decorator(cls._modifiers, part)
            parts = parts[(len(parts) - parts[-1::-1].index(cls._modifier_splitter) - 1) + 2:]

        if "on" in parts:
            backcolor = cls._translate_to_ansi_decorator(cls._backcolors, parts[parts.index(cls._backcolor_splitter) + 1])
            parts = parts[:-2]

        if len(parts) > 0:
            forecolor = cls._translate_to_ansi_decorator(cls._forecolors, parts[0])

        return modifiers + forecolor + backcolor + "%s" + cls._translate_to_ansi_decorator(cls._modifiers, "reset")

    @classmethod
    def encode(cls, string):
        if isinstance(string, unicode):
            string = string.encode("utf-8")
        return string


class ColorfulMeta(type):
    colors = True

    class _ColorfulOut(type):
        def __getattr__(cls, attr):
            def decorated_text(text):
                output = text
                output = ColorfulParser.parse_attr(attr) % (text)

                print(ColorfulParser.encode(output))
                sys.stdout.flush()
            return decorated_text

    out = _ColorfulOut("out", (object, ), {})

    def __getattr__(cls, attr):
        def decorated_text(text):
            output = text
            output = ColorfulParser.parse_attr(attr) % (text)
            return ColorfulParser.encode(output)
        return decorated_text

colorful = ColorfulMeta("cf", (object, ), {})
