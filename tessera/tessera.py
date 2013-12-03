# -*- coding: utf-8 -*-

import os
import re

from sys import stderr

from colorful import colorful

from exceptions import TesseraError


class Tessera(object):
    _tesserae = None

    def __init__(self, tessera_path, config):
        self.tessera_path = tessera_path
        self._config = config
        self.filename = "%s/tessera" % tessera_path
        self.mtime = os.lstat(self.filename).st_mtime
        self.tessera_hash = os.path.basename(self.tessera_path)
        self._attributes = {}

        self._read()
        self._parse()

    def get_attribute(self, attribute):
        return self._attributes.get(attribute, "no %s" % attribute)

    def _read(self):
        if not os.path.exists(self.filename):
            stderr.write("tessera file not found: %s\n" % self.fielname)
            return None

        f = open(self.filename, 'r')
        self.body = f.read().split('\n')
        f.close()

    def _parse(self):
        self._attributes["tags"] = set()
        self.content = []
        title_pattern = re.compile("^# (?P<title>.*)$")
        status_pattern = re.compile("^@status (?P<status>.*)$")
        type_pattern = re.compile("^@type (?P<type>.*)$")
        tags_pattern = re.compile("^@tags (?P<tags>.*)$")
        in_header = True
        for l in self.body:
            if in_header:
                if not l.strip():
                    continue

                title_match = title_pattern.search(l)
                if title_match:
                    self._attributes["title"] = title_match.groupdict()["title"]
                    continue
                status_match = status_pattern.search(l)
                if status_match:
                    self._attributes["status"] = status_match.groupdict()["status"]
                    continue
                type_match = type_pattern.search(l)
                if type_match:
                    self._attributes["type"] = type_match.groupdict()["type"]
                    continue
                tags_match = tags_pattern.search(l)
                if tags_match:
                    self._attributes["tags"] = set([x.strip() for x in tags_match.groupdict()["tags"].split(",")])
                    continue

                in_header = False
            self.content.append(l)
        self.content = "\n".join(self.content)

        # FIXME: fix status id, why do we need this?
        self.status_id = -1

        # FIXME: fix type id, why do we need this?
        self.te_type_id = -1

    def _write(self):
        with open(self.filename, "w") as f:
            f.write("# %s\n" % self.get_attribute("title"))
            f.write("@status %s\n" % self.get_attribute("status"))
            f.write("@type %s\n" % self.get_attribute("type"))
            f.write("@tags %s\n" % ", ".join(self._attributes["tags"]))
            f.write("\n%s" % self.content)

    def summary(self):
        title = self.get_attribute("title")
        status = self.get_attribute("status")
        te_type = self.get_attribute("type")
        len_title = len(title)
        len_status = len(status)
        tags = ", ".join(self._attributes["tags"])
        try:
            color_status = self._config.get("color \"status\"", status)
        except TesseraError, e:
            colorful.out.bold_red(e)
            return
        if color_status:
            if colorful.exists(color_status):
                status = colorful.get(color_status)(status)

        try:
            color_type = self._config.get("color \"type\"", te_type)
        except TesseraError, e:
            colorful.out.bold_red(e)
            return
        if color_type:
            if colorful.exists(color_type):
                title = colorful.get(color_type)(title)

        return "%s %s %s %s %s %s %s %s" % (self.get_ident_short(), title, " " * (40 - len_title), status, " " * (10 - len_status), te_type, " " * (10 - len(te_type)), tags)

    def add_tag(self, tag):
        self._attributes["tags"].add(tag)
        self._write()
        return True

    def ident(self):
        return dict(ident=self.tessera_hash, title=self.get_attribute("title"), filename=self.filename, body=self.get_body())

    def get_ident_short(self):
        return self.tessera_hash.split('-')[0]
