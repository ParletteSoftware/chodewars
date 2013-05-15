import logging
import db

from player import Player

class Game(object):
  def __init__(self):
    #Setup logging for this module
    self.log = logging.getLogger('chodewars.game')
    self.log.setLevel(logging.DEBUG)
    
    #Log Format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    #Log to File
    fh = logging.FileHandler('chodewars.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    
    #Log to Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)
    
    self.log.addHandler(fh)
    self.log.addHandler(ch)
    
    #Setup instance variables
    self.db = None
  
  def load_config(self):
    self.log.debug("Loading configuration")
    self.db_type = "file"
    if self.db_type is "file":
      self.log.info('Using flat file database')
      self.db = db.FlatFileDatabase(location = "data",
                                    name = "universe")
    return True
  
  def connect_db(self):
    if self.db:
      self.log.debug('Connecting to database')
      return self.db.connect()
    else:
      self.log.error("There is no database defined")
      return False
  
  def big_bang(self):
    if self.db:
      self.log.info("Executing Big Bang")
      return self.db.big_bang()
  
  def add_player(self,player):
    if self.db and player:
      self.log.debug("Adding player %s" % player.name)
      return self.db.add_player(player)
  
  def get_player_by_id(self,player_id):
    if self.db:
      self.log.debug("Retrieving player account for id %s" % player_id)
      return self.db.get_player_by_id(player_id)
