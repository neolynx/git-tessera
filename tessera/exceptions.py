# -*- coding: utf-8 -*-


class TesseraError(Exception):
    def __init__(self, message=None):
        self._message = "An undefined error occured" if message is None else message

    def __str__(self):
        return self._message


class ArgumentError(TesseraError):
    def __init__(self, message):
        self._message = message


class ConfigFileNotFoundError(TesseraError):
    def __init__(self, path):
        self._message = "Could not find config file at '%s'" % path


class ConfigSectionNotFoundError(TesseraError):
    def __init__(self, section, path):
        self._message = "Could not find section %s in config file %s" % (section, path)


class ConfigOptionNotFoundError(TesseraError):
    def __init__(self, attribute, section, path):
        self._message = "Could not find option '%s' in section '%s' in config file '%s'" % (attribute, section, path)
