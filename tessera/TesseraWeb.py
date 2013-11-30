import web
import markdown
import sys
from os import path
from GitTessera import GitTessera

render = web.template.render('%s/web'%path.dirname(path.realpath(__file__)))

class TesseraWeb(object):
  def __init__(self):
    self.urls = ('/', 'index',
                 '/tessera.css', 'css')

  def serve(self):
    sys.argv = []
    app = web.application(self.urls, globals())
    app.run()

class index(object):
  def GET(self):
    html = ""
    gt = GitTessera()
    tesserae = gt.ls()
    return render.index(tesserae)


class css:
  def GET(self):
    f = open('%s/web/tessera.css'%path.dirname(path.realpath(__file__)), "r" )
    stylesheet = f.read()
    f.close()
    return stylesheet

