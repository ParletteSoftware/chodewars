import logging
import db

class Game(object):
  def __init__(self):
    #Setup logging for this module
    self.log = logging.getLogger('chodewars.game')
    self.log.setLevel(logging.DEBUG)
    fh = logging.FileHandler('chodewars.log')
    fh.setLevel(logging.DEBUG)
    self.log.addHandler(fh)
    
    #Setup instance variables
    self.db = None
  
  def load_config(self):
    self.log.debug("Loading configuration")
    self.db_type = "file"
    if self.db_type is "file":
      self.log.info('Using flat file database')
      self.db = db.FlatFileDatabase(location = "data",
                                    name = "u")
  
  def connect_db(self):
    if self.db:
      self.log.debug('Connecting to database')
      self.db.connect()
    else:
      self.log.error("There is no database defined")
  
