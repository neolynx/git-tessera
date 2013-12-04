# -*- coding: utf-8 -*-

from exceptions import ConfigFileNotFoundError, ConfigSectionNotFoundError, ConfigOptionNotFoundError

import os
from ConfigParser import ConfigParser, NoSectionError, NoOptionError


class TesseraConfig(object):
    def __init__(self, path):
        self._path = path
        self._config = ConfigParser()
        if os.path.exists(path):
            self._parse()

    def get_path(self):
        return self._path

    def _parse(self):
        self._config.read(self._path)

    def has_option(self, section, option):
        try:
            self._config.get(section, option)
            return True
        except:
            return False

    def get(self, section, option):
        try:
            return self._config.get(section, option)
        except NoSectionError:
            raise ConfigSectionNotFoundError(section, self._path)
        except NoOptionError:
            raise ConfigOptionNotFoundError(option, section, self._path)

    def get_section(self, section):
        try:
            return self._config.get(section)
        except NoSectionError:
            raise ConfigSectionNotFoundError(section, self._path)

    def set(self, section, option, value):
        self._config[section][option] = value

    def store(self):
        with open(self._path, "w") as f:
            self._config.write(f)
