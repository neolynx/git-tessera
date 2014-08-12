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
        self.error = False
        self.body = []
        self.info = []
        self.update()

    def get_attribute(self, attribute):
        return self._attributes.get(attribute, None)

    def update(self):
        self._read()
        return self._parse()

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

        self.error = False
        for k, v in attributes.items():
            if k == "status":
                idx = self._config.get_option_index("status", v)
                if idx == -1:
                    print "%s: invalid status: %s" % (self.filename ,v)
                    self.error = True
                    continue
                self._attributes["status"] = v
                self._attributes["status_id"] = idx
            elif k == "type":
                idx = self._config.get_option_index("types", v)
                if idx == -1:
                    print "%s: invalid type: %s" % (self.filename ,v)
                    self.error = True
                    continue
                self._attributes["type"] = v
                self._attributes["type_id"] = idx
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
        return not self.error


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
        status = self.get_attribute("status")
        te_type = self.get_attribute("type")

        if not title:
            title = "untitled"
        l_title = len(title)

        if not status:
            status = "no status"
        l_status = len(status)
        try:
            color_status = self._config.get("status", status)
        except TesseraError, e:
            color_status = "red"
        if color_status and colorful.exists(color_status):
            status = colorful.get(color_status)(status)

        if not te_type:
            te_type = "no type"
        l_type = len(te_type)
        try:
            color_type = self._config.get("types", te_type)
        except TesseraError, e:
            color_type = "red"
            te_type = colorful.get(color_type)(te_type)

        if color_type and colorful.exists(color_type):
            title = colorful.get(color_type)(title)

        author = self._attributes["author"]
        l_author = len(author)

        tags = ", ".join(self._attributes["tags"])

        return "%s %s %s %s %s %s %s %s %s %s" % (self.get_ident_short(),
                                               title,   " " * (60 - l_title),
                                               status,  " " * (10 - l_status),
                                               te_type, " " * (10 - l_type),
                                               author,  " " * (20 - l_author),
                                               tags)

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
