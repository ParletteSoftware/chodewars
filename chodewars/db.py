import os
import logging

class Database(object):
  """This is a base class which defines the methods that need to be implemented for database operations.
  
  For example, a class Mongo(Database) would define database operations for a mongodb,
  or a class File(Database) would define operations for a flat file database.
  
  To program the game to support any of the databases, only the methods defined in the Database base class should be used to avoid any database-specific code."""
  
  def __init__(self,name,location):
    #Setup logging for this module
    self.create_logger("chodewars.db.%s" % self.__class__.__name__)
    
    #Database name
    self.name = name
    
    #Location of the database (server address, file path)
    self.location = location
  
  def create_logger(self,name):
    self.log = logging.getLogger(name)
    self.log.setLevel(logging.DEBUG)
    fh = logging.FileHandler('chodewars.log')
    fh.setLevel(logging.DEBUG)
    self.log.addHandler(fh)
  
  def connect(self):
    """Connect to the database."""
    pass
  
  def big_bang(self):
    """Delete the database and create it from scratch."""
    pass
  
  def add_player(self):
    """Add a player to the database."""
    pass
  
  def get_player(self,player_id = None):
    """Retrieve a player account."""
    pass
  
  def get_sector(self,sector = None):
    """Retrieve a list of all items in a sector."""
    pass
  
class FlatFileDatabase(Database):
  def connect(self):
    """Make sure the self.location exists, and has a self.name directory in it."""
    self.log.debug("Creating directory %s" % os.path.join(self.location,self.name))
    os.makedirs(os.path.join(self.location,self.name))
