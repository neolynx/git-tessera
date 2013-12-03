# -*- coding: utf-8 -*-

import web
import sys
from os import path
from gittessera import GitTessera
import markdown

render = web.template.render('%s/web' % path.dirname(path.realpath(__file__)))


class TesseraWeb(object):
    def __init__(self):
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
        gt = GitTessera()
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
        i = web.input(key=None)
        gt = GitTessera()
        tessera = gt.get(i.key)
        if not tessera:
            return "not found"
        render = web.template.render('%s/web' % path.dirname(path.realpath(__file__)))
        tessera.markdown = markdown.markdown(tessera.content)
        return render.detail(tessera)
