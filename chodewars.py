import tornado.ioloop
import tornado.web
import os.path
import logging
import datetime

from tornado.options import define,options

define("port", default=9000, help="run on the given port", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    handlers=[
      (r"/", MainHandler),
    ]
    
    settings = dict(
      template_path = os.path.join(os.path.dirname(__file__), "templates"),
      static_path = os.path.join(os.path.dirname(__file__), "static"),
      debug = True,
    )
    tornado.web.Application.__init__(self,handlers,**settings)

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render(
      "index.html",
      page_title = "Here's a page",
      header_text = "Heading",
      footer_text = "Chodewars",
    )

if __name__ == "__main__":
  app = Application()
  app.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
