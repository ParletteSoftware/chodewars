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
    self.path = os.path.join(self.location,self.name)
    if not os.path.exists(self.path):
      self.log.debug("Creating directory %s" % self.path)
      os.makedirs(self.path)
      
    if os.path.exists(self.path):
      return True
    else:
      self.log.error("Database directory (%s) could not be created" % self.path)
      return False
  
  def big_bang(self):
    """Delete all of the files in the directory."""
    if self.path:
      if os.path.exists(self.path):
        self.log.debug("Importing shutil")
        shutil = __import__('shutil')
        self.log.debug("Removing directory (%s) contents" % self.path)
        shutil.rmtree(self.path)
      else:
        self.log.debug("Path %s does not exist, creating it..." % self.path)
        os.makedirs(self.path)
    else:
      self.log.error("FlatFileDatabase instance variable 'path' is not defined")
      return False
    
    #Create the universe
    ##nothing to do yet
    return True
