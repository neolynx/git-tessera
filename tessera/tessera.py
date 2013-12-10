# -*- coding: utf-8 -*-

import os
import re
from time import time
from sys import stderr

from colorful import colorful

from exceptions import TesseraError


class Tessera(object):
    _tesserae  = None
    re_title   = re.compile("^# (?P<title>.+)$")
    re_status  = re.compile("^@status (?P<status>.*)$")
    re_type    = re.compile("^@type (?P<type>.+)$")
    re_tags    = re.compile("^@tags (?P<tags>.+)$")
    re_author  = re.compile("^author: (.+)$")
    re_email   = re.compile("^email: (.+)$")
    re_updated = re.compile("^updated: (\d+)$")

    def __init__(self, tessera_path, config):
        self.tessera_path = tessera_path
        self._config = config
        self.tessera_hash = os.path.basename(self.tessera_path)
        self.filename = os.path.join(self.tessera_path, "tessera")
        self.infofile = os.path.join(self.tessera_path, "info")
        self._attributes = { "author": "unknown", "email": "", "updated": 0 }
        self.body = []
        self.info = []
        self.update()

    def get_attribute(self, attribute):
        return self._attributes.get(attribute, "no %s" % attribute)

    def update(self):
        self._read()
        self._parse()

    def _read(self):
        if not os.path.exists(self.filename):
            raise TesseraError("tessera file not found: %s" % self.filename)

        f = open(self.filename, 'r')
        self.body = f.read().split('\n')
        f.close()

        if os.path.exists(self.infofile):
            f = open(self.infofile, 'r')
            self.info = f.read().split('\n')
            f.close()

    def _parse(self):
        self._attributes["tags"] = set()
        self.content = []
        in_header = True
        for l in self.body:
            l = l.strip()
            if in_header:
                if not l:
                    continue

                title_match = self.re_title.search(l)
                if title_match:
                    self._attributes["title"] = title_match.groupdict()["title"]
                    continue
                status_match = self.re_status.search(l)
                if status_match:
                    self._attributes["status"] = status_match.groupdict()["status"]
                    self._attributes["status_id"] = self._config.get_option_index("status", self._attributes["status"])
                    continue
                type_match = self.re_type.search(l)
                if type_match:
                    self._attributes["type"] = type_match.groupdict()["type"]
                    self._attributes["type_id"]   = self._config.get_option_index("types", self._attributes["type"])
                    continue
                tags_match = self.re_tags.search(l)
                if tags_match:
                    self._attributes["tags"] = set([x.strip() for x in tags_match.groupdict()["tags"].split(",")])
                    continue

                in_header = False
            self.content.append(l)
        self.content = "\n".join(self.content)

        for l in self.info:
            l = l.strip()
            if not l:
                continue
            m = self.re_author.search(l)
            if m:
                self._attributes["author"] = m.group(1)
                continue
            m = self.re_email.search(l)
            if m:
                self._attributes["author_email"] = m.group(1)
                continue
            m = self.re_updated.search(l)
            if m:
                self._attributes["updated"] = m.group(1)
                continue


    def _write(self):
        self._write_tessera()
        self._write_info()

    def _write_tessera(self):
        with open(self.filename, "w") as f:
            f.write("# %s\n" % self.get_attribute("title"))
            f.write("@status %s\n" % self.get_attribute("status"))
            f.write("@type %s\n" % self.get_attribute("type"))
            f.write("@tags %s\n" % ", ".join(self._attributes["tags"]))
            f.write("\n%s" % self.content)

    def _write_info(self):
        with open(self.infofile, "w") as f:
            f.write("author: %s\n" % self.get_attribute("author"))
            f.write("email: %s\n" % self.get_attribute("author_email"))
            f.write("updated: %d\n" % int(time()))

    def summary(self):
        title = self.get_attribute("title")
        status = self.get_attribute("status")
        te_type = self.get_attribute("type")
        len_title = len(title)
        len_status = len(status)
        tags = ", ".join(self._attributes["tags"])
        try:
            color_status = self._config.get("status", status)
        except TesseraError, e:
            colorful.out.bold_red(e)
            return
        if color_status:
            if colorful.exists(color_status):
                status = colorful.get(color_status)(status)

        try:
            color_type = self._config.get("types", te_type)
        except TesseraError, e:
            colorful.out.bold_red(e)
            return
        if color_type:
            if colorful.exists(color_type):
                title = colorful.get(color_type)(title)

        return "%s %s %s %s %s %s %s %s %s" % (self.get_ident_short(), title, " " * (60 - len_title), status, " " * (10 - len_status), te_type, " " * (10 - len(te_type)), self._attributes["author"], tags)

    def add_tag(self, tag):
        self._attributes["tags"].add(tag)
        self._write()
        return True

    def ident(self):
        return dict(
            ident=self.tessera_hash,
            title=self.get_attribute("title"),
            filename=self.filename,
            body=self.body)

    def get_ident_short(self):
        return self.tessera_hash.split('-')[0]
