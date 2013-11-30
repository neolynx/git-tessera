import web
import markdown
import sys
from os import path
from gittessera import GitTessera

render = web.template.render('%s/web'%path.dirname(path.realpath(__file__)))

class TesseraWeb:
  def __init__(self):
    self.urls = ('/', 'index')

  def serve(self):
    sys.argv = []
    app = web.application(self.urls, globals())
    app.run()

class index:
  def GET(self):
    html = ""
    gt = GitTessera()
    tesserae = gt.ls()
    return render.index(tesserae)



