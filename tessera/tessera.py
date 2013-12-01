# -*- coding: utf-8 -*-

import os
import re

from sys import stderr

from colorful import colorful


class Tessera(object):
    _tesserae = None
    _status = {}
    _te_types = {}

    def __init__(self, tessera_path):
        self.tessera_path = tessera_path
        self.filename = "%s/tessera" % tessera_path
        self.mtime = os.lstat(self.filename).st_mtime
        self.tessera_hash = os.path.basename(self.tessera_path)
        self.title = None
        self.status = None
        self.te_type = None

        if not self._status:
            self._read_status()

        if not self._te_types:
            self._read_types()

        self._read()
        self._parse()

    def _read_status(self):
        status_file = "%s/status" % Tessera._tesserae
        Tessera._status = self._read_config(status_file)

    def _read_types(self):
        types_file = "%s/types" % Tessera._tesserae
        Tessera._te_types = self._read_config(types_file)

    def _read_config(self, filename):
        if not os.path.exists(filename):
            colorful.out.bold_red("file not found: %s" % filename)
            Tessera._te_types = False
            return

        config = {}
        with open(filename, 'r') as f:
            i = 0
            for line in f.readlines():
                line = line.strip()
                if line:
                    a = re.split(r'[ \t]+', line)
                    if len(a) != 2:
                        colorful.out.bold_red("Error in %s: invalid status line: %s" % (filename, line))
                        break
                    if not colorful.exists(a[1]):
                        colorful.out.bold_red("Error in %s: color %s does not exist" % (filename, a[1]))
                        break
                    config[i] = (a[0], a[1])
                    i += 1
        return config

    def _read(self):
        if not os.path.exists(self.filename):
            stderr.write("tessera file not found: %s\n" % self.fielname)
            return None

        f = open(self.filename, 'r')
        self.body = f.read().split('\n')
        f.close()

    def _parse(self):
        self.title = "no title"
        self.status = ""
        self.te_type = ""
        self.tags = set()
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
                    self.title = title_match.groupdict()["title"]
                    continue
                status_match = status_pattern.search(l)
                if status_match:
                    self.status = status_match.groupdict()["status"]
                    continue
                type_match = type_pattern.search(l)
                if type_match:
                    self.te_type = type_match.groupdict()["type"]
                    continue
                tags_match = tags_pattern.search(l)
                if tags_match:
                    self.tags = set([x.strip() for x in tags_match.groupdict()["tags"].split(",")])
                    continue

                in_header = False
            self.content.append(l)
        self.content = "\n".join(self.content)

        self.status_id = -1
        if not self.status:
            self.status = "no status"
        else:
            for key, val in Tessera._status.iteritems():
                if val[0] == self.status:
                    self.status_id = key
                    break

        self.te_type_id = -1
        if not self.te_type:
            self.te_type = "no te_type"
        else:
            for key, val in Tessera._te_types.iteritems():
                if val[0] == self.te_type:
                    self.te_type_id = key
                    break

    def _write(self):
        with open(self.filename, "w") as f:
            f.write("# %s\n" % self.title)
            f.write("@status %s\n" % self.status)
            f.write("@type %s\n" % self.te_type)
            f.write("@tags %s\n" % ", ".join(self.tags))
            f.write("\n%s" % self.content)

    def summary(self):
        len_title = len(self.title)
        len_status = len(self.status)
        tags = ", ".join(self.tags)
        title = self.title
        color = None
        if Tessera._status:
            for s in Tessera._status:
                if Tessera._status[s][0] == self.status:
                    color = Tessera._status[s][1]
                    break
            status = self.status
        else:
            status = "no status available"
        if color:
            if colorful.exists(color):
                status = colorful.get(color)(self.status)

        color = None
        if Tessera._te_types:
            for s in Tessera._te_types:
                if Tessera._te_types[s][0] == self.te_type:
                    color = Tessera._te_types[s][1]
                    break
            te_type = self.te_type
        else:
            te_type = "no type available"
        if color:
            if colorful.exists(color):
                title = colorful.get(color)(title)

        return "%s %s %s %s %s %s %s %s" % (self.get_ident_short(), title, " " * (40 - len_title), status, " " * (10 - len_status), te_type, " " * (10 - len(te_type)), tags)

    def add_tag(self, tag):
        self.tags.add(tag)
        self._write()
        return True

    def ident(self):
        return dict(ident=self.tessera_hash, title=self.title, filename=self.filename, body=self.get_body())

    def get_ident_short(self):
        return self.tessera_hash.split('-')[0]

    def get_body(self):
        return '\n'.join(self.body)
