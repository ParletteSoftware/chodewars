import tornado.ioloop
import tornado.web
import tornado.auth
import os.path
import logging
import datetime
import sys
import argparse

from tornado.options import define,options
from chodewars.game import Game
from chodewars.player import Player
from chodewars.planet import Planet

define("port", default=9000, help="run on the given port", type=int)

version = "0.0"

game = None

class Application(tornado.web.Application):
  def __init__(self):
    handlers=[
      (r"/", MainHandler),
      (r"/login", LoginHandler),
      (r"/logout", LogoutHandler),
      (r"/add/([\w]*)", AddHandler),
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
    {u'email': u'matthew.parlette@gmail.com',
    u'first_name': u'Matthew',
    u'last_name': u'Parlette',
    u'claimed_id': u'https://www.google.com/accounts/o8/id?id=AItOawn5BtKjHuaIP870Gex-U3jwWKLi2X2pqGw',
    u'name': u'Matthew Parlette'}"""
    if not user_json: return None
    return tornado.escape.json_decode(user_json)
  
  def get_current_player(self):
    if not self.current_user: return None
    if not game: return None
    if 'email' in self.current_user:
      return game.get_player_by_id(self.current_user['email'])
    else:
      #If email doesn't exist in the cookie, then it needs to be refreshed
      self.clear_cookie('user')
      self.redirect("/")
    return None

class MainHandler(BaseHandler):
  @tornado.web.authenticated
  def get(self):
    self.render(
      "index.html",
      page_title = "Here's a page",
      header_text = "Heading",
      footer_text = "Chodewars",
      user = self.current_user,
      player = self.get_current_player(),
    )

class LoginHandler(BaseHandler, tornado.auth.GoogleMixin):
  @tornado.web.asynchronous
  def get(self):
    if self.get_argument("openid.mode", None):
      self.get_authenticated_user(self.async_callback(self._on_auth))
      return
    self.authenticate_redirect(ax_attrs=["name","email"])

  def _on_auth(self, user):
    if not user:
      raise tornado.web.HTTPError(500, "Google auth failed")
    self.set_secure_cookie("user", tornado.escape.json_encode(user))
    self.redirect("/")

class LogoutHandler(BaseHandler):
  def get(self):
    self.clear_cookie("user")
    self.write("You are now logged out")

class AddHandler(BaseHandler):
  #@tornado.web.authenticated
  def get(self,add_type):
    self.render(
      "add.html",
      page_title = "Add Something",
      header_text = "Create",
      footer_text = "Chodewars",
      user = self.current_user,
      add_type = add_type,
    )
  
  def post(self,add_type):
    if game:
      if add_type == "player":
        name = self.get_argument('name','')
        print "Creating new player %s..." % name
        if game.add_player(Player(self.current_user['email'],name)):
          print "Player %s created" % name
        else:
          print "Error creating player %s" % name
      else:
        if add_type == "home":
          planet_name = self.get_argument('planet_name',None)
          if planet_name:
            player = self.get_current_player()
            print "Creating home sector..."
            if game.assign_home_sector(player,planet_name):
              print "...ok"
            else:
              print "Error assigning home sector for %s" % str(player)
          else:
            print "planet_name was not received, nothing was created for this player"
    else:
      print "Game is not initialized!"
        
    self.redirect("/")

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Process command line options.')
  parser.add_argument('--bigbang', action='store_true', help='Execute a Big Bang, this deletes an existing universe and creates a new one.')
  parser.add_argument('--version', action='version', version='Chodewars v'+version)
  args = parser.parse_args()
  
  print "Creating game object..."
  game = Game()
  if game:
    print "...ok"
  else:
    print "error initializing game"
    sys.exit(1)
  
  if args.bigbang:
    print "Executing Big Bang..."
    game.big_bang()
    print "...ok"
    sys.exit(0)
  
  print "Game created, listening for connections..."
  app = Application()
  app.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
