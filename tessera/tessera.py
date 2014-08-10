# -*- coding: utf-8 -*-

from os import path

from exceptions import TesseraError

class Tessera(object):
    _tesserae  = None
    keywords  = {
        "# "       : "title",
        "@status " : "status",
        "@type "   : "type",
        "@tags "   : "tags",
    }
    info = {
        "author"  : "author: ",
        "email"   : "email: ",
        "updated" : "updated: ",
    }

    def __init__(self, tessera_path, config):
        self.tessera_path = tessera_path
        self._config = config
        self.tessera_hash = path.basename(self.tessera_path)
        self.filename = path.join(self.tessera_path, "tessera")
        self.infofile = path.join(self.tessera_path, "info")
        self._attributes = { "author": "unknown", "email": "", "updated": 0, "tags": "" }
        self.body = []
        self.info = []
        self.update()

    def get_attribute(self, attribute):
        return self._attributes.get(attribute, "no %s" % attribute)

    def update(self):
        self._read()
        self._parse()

    def _read(self):
        if not path.exists(self.filename):
            raise TesseraError("tessera file not found: %s" % self.filename)

        f = open(self.filename, 'r')
        self.body = f.read().split('\n')
        f.close()

        if path.exists(self.infofile):
            f = open(self.infofile, 'r')
            self.info = f.read().split('\n')
            f.close()

    def _parse(self):
        content = []
        keywords = Tessera.keywords.keys()
        attributes = {}
        for l in self.body:
            comment = l.find("//")
            if comment != -1:
                l = l[0 : comment]
            l = l.strip()
            if not l:
                continue

            kw = False
            if l[0] == "@" or l[0] == "#":
                for k in keywords:
                    if l.startswith( k ):
                        attributes[Tessera.keywords[k]] = l[len(k):]
                        keywords.remove( k )
                        kw = True
                        break

            if not kw:
                content.append(l)

        self.content = "\n".join(content)

        for k, v in attributes.items():
            if k == "status":
                self._attributes["status_id"] = self._config.get_option_index("status", v)
            elif k == "type":
                self._attributes["type_id"] = self._config.get_option_index("types", v)
            elif k == "tags":
                self._attributes[k] = set([x.strip() for x in v.split(",")])
            else:
                self._attributes[k] = v
        for l in self.info:
            l = l.strip()
            if not l:
                continue
            for k, v in Tessera.info.iteritems():
                if l.startswith( v ):
                    self._attributes[k] = l[len(v):]
                    break


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
            from time import time
            f.write("author: %s\n" % self.get_attribute("author"))
            f.write("email: %s\n" % self.get_attribute("author_email"))
            f.write("updated: %d\n" % int(time()))

    def summary(self):
        from colorful import colorful
        title = self.get_attribute("title")
        status = self._config.get_option_name( "status", self.get_attribute("status_id"))
        te_type = self._config.get_option_name( "types", self.get_attribute("type_id"))
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
