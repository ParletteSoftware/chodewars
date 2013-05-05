import tornado.ioloop
import tornado.web
import tornado.auth
import os.path
import logging
import datetime

from tornado.options import define,options

define("port", default=9000, help="run on the given port", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    handlers=[
      (r"/", MainHandler),
      (r"/login", LoginHandler),
      (r"/logout", LogoutHandler)
    ]
    
    settings = dict(
      template_path = os.path.join(os.path.dirname(__file__), "templates"),
      static_path = os.path.join(os.path.dirname(__file__), "static"),
      cookie_secret = "43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
      login_url = "/login",
      debug = True,
    )
    tornado.web.Application.__init__(self,handlers,**settings)

class BaseHandler(tornado.web.RequestHandler):
  def get_current_user(self):
    user_json = self.get_secure_cookie("user")
    """user_json is of the form:
    {u'first_name': u'Matthew',
    u'last_name': u'Parlette',
    u'claimed_id': u'https://www.google.com/accounts/o8/id?id=AItOawn5BtKjHuaIP870Gex-U3jwWKLi2X2pqGw',
    u'name': u'Matthew Parlette'}"""
    if not user_json: return None
    return tornado.escape.json_decode(user_json)

class MainHandler(BaseHandler):
  @tornado.web.authenticated
  def get(self):
    self.render(
      "index.html",
      page_title = "Here's a page",
      header_text = "Heading",
      footer_text = "Chodewars",
      username = self.current_user,
    )

class LoginHandler(BaseHandler, tornado.auth.GoogleMixin):
  @tornado.web.asynchronous
  def get(self):
    if self.get_argument("openid.mode", None):
      self.get_authenticated_user(self.async_callback(self._on_auth))
      return
    self.authenticate_redirect(ax_attrs=["name"])

  def _on_auth(self, user):
    if not user:
      raise tornado.web.HTTPError(500, "Google auth failed")
    self.set_secure_cookie("user", tornado.escape.json_encode(user))
    self.redirect("/")

class LogoutHandler(BaseHandler):
  def get(self):
    self.clear_cookie("user")
    self.write("You are now logged out")

if __name__ == "__main__":
  app = Application()
  app.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
