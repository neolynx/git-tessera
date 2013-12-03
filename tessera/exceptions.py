# -*- coding: utf-8 -*-


class TesseraError(Exception):
    def __init__(self):
        self._message = "An undefined error occured"

    def __str__(self):
        return self._message


class ConfigFileNotFoundError(TesseraError):
    def __init__(self, path):
        self._message = "Could not found config file at '%s'" % path


class ConfigSectionNotFoundError(TesseraError):
    def __init__(self, section, path):
        self._message = "Could not found section %s in config file %s" % (section, path)


class ConfigOptionNotFoundError(TesseraError):
    def __init__(self, attribute, section, path):
        self._message = "Could not found option %s in section %s in config file %s" % (attribute, section, path)
