# -*- coding: utf-8 -*-

import web
import sys
from os import path
from tessera import Tessera
from tesseraconfig import TesseraConfig
from gittessera import GitTessera
import markdown

render = web.template.render('%s/web' % path.dirname(path.realpath(__file__)))


class TesseraWeb(object):
    def __init__(self):
        git_directory = "."
        Tessera._tesserae = path.relpath(path.join(git_directory, ".tesserae"))
        self.urls = ('/', 'index',
                     '/style/tessera.css', 'css',
                     '/tessera(.*)', 'tessera'
                    )

    def serve(self):
        sys.argv = []
        app = web.application(self.urls, globals())
        app.run()


class index(object):
    def GET(self):
        self._config = TesseraConfig(path.join(Tessera._tesserae, "config"))
        gt = GitTessera(self._config)
        tesserae = gt.ls()
        return render.index(tesserae)


class css:
    def GET(self):
        f = open('%s/web/style/tessera.css' % path.dirname(path.realpath(__file__)), "r")
        stylesheet = f.read()
        f.close()
        return stylesheet


class tessera:
    def GET(self, key):
        self._config = TesseraConfig(path.join(Tessera._tesserae, "config"))
        i = web.input(key=None)
        gt = GitTessera(self._config)
        tessera = gt.get(i.key)
        if not tessera:
            return "not found"
        render = web.template.render('%s/web' % path.dirname(path.realpath(__file__)))
        tessera.markdown = markdown.markdown(tessera.content)
        return render.detail(tessera)
