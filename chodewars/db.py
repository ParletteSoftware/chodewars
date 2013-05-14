import os
import logging

from player import Player

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
  
  def db_exists(self):
    """Return a boolean to signify if the database exists."""
    pass
  
  def connect(self):
    """Connect to the database."""
    pass
  
  def big_bang(self):
    """Delete the database and create it from scratch."""
    pass
  
  def is_empty(self):
    """Return a boolean to signify if the database is empty (and requires a big bang)."""
    pass
  
  def add_player(self,player):
    """Add a player to the database."""
    pass
  
  def get_player(self,player_name = None):
    """Retrieve a player account."""
    return None
  
  def get_player_by_id(self,player_id):
    """Retrieve a player account by id."""
    return None
  
  def get_sector(self,sector = None):
    """Retrieve a list of all items in a sector."""
    pass
  
class FlatFileDatabase(Database):
  def db_exists(self):
    if self.path:
      if os.path.exists(self.path):
        self.log.debug("db_exists(): %s exists, returning True" % self.path)
        return True
    else:
      self.log.error("db_exists(): FlatFileDatabase instance variable 'path' is not defined")
      return False
    
  def connect(self):
    """Make sure the self.location exists, and has a self.name directory in it."""
    self.path = os.path.join(self.location,self.name)
    if not os.path.exists(self.path):
      self.log.debug("Creating directory %s" % self.path)
      os.makedirs(self.path)
      
    if os.path.exists(self.path):
      if self.is_empty():
        self.log.info("Universe appears to be empty, executing Big Bang.")
        return self.big_bang()
      return True
    else:
      self.log.error("Database directory (%s) could not be created" % self.path)
      return False
  
  def big_bang(self):
    """Delete all of the files in the directory."""
    if self.path:
      if os.path.exists(self.path):
        self.log.debug("Removing directory (%s) contents" % self.path)
        for f in os.listdir(self.path):
          os.remove(f)
      else:
        self.log.debug("Path %s does not exist, creating it..." % self.path)
        os.makedirs(self.path)
    else:
      self.log.error("FlatFileDatabase instance variable 'path' is not defined")
      return False
    
    #Create the universe
    ##nothing to do yet
    return True
  
  def is_emtpy(self):
    """Return true if the data directory is empty."""
    if self.path:
      if os.path.exists(self.path):
        if os.listdir(self.path):
          #A non-empty list was returned, meaning there are files there
          self.log.debug("Path %s seems to have files in it, is_empty() returning False" % self.path)
          return False
        else:
          #Empty list, no files in dir
          self.log.debug("Path %s seems to have no files in it, is_empty() returning True" % self.path)
          return True
      else:
        self.log.debug("Path %s does not exist, so returning True" % self.path)
        return True
    else:
      self.log.error("FlatFileDatabase instance variable 'path' is not defined")
      return False
  
  def add_player(self,player):
    """Create a file for the player if it doesn't already exist."""
    if self.db_exists():
      if self.get_player(player.name) is None:
        if self._write_player(player,"%s.player" % player.name):
          self.log.debug("add_player(): Player %s successfully added" % player.name)
          return True
        else:
          self.log.error("add_player(): Error writing to player file")
          return False
      else:
        self.log.error("add_player(): Player already exists")
        return False
    else:
      self.log.error("add_player(): Database does not exist, aborting...")
      return False
  
  def _write_player(self,player,filename):
    """Wrtie the player object to file, overwriting whatever is there."""
    self.log.debug("_write_player(): Opening %s for writing" % os.path.join(self.path,filename))
    f = open(os.path.join(self.path,filename),'w')
    with f:
      f.write("%s\n" % player.id)
      f.write("%s\n" % player.name)
      f.close()
      return True
    self.log.error("_write_player(): Error opening %s for writing" % os.path.join(self.path,filename))
    return False
  
  def get_player(self,player_name):
    """Verify a player file exists and load that Player object."""
    if self.db_exists():
      player_file_path = os.path.join(self.path,"%s.player" % player_name)
      if os.path.exists(player_file_path):
        self.log.debug("get_player(): Player file %s was found, calling _read_player()" % player_file_path)
        return self._read_player("%s.player" % player_name)
      else:
        self.log.debug("get_player(): Player file %s was not found, returning None" % player_file_path)
        return None
    else:
      self.log.error("get_player(): Database does not exist, aborting...")
      return None
  
  def get_player_by_id(self,player_id):
    """Go through each .player file to find the specified id."""
    for f in os.listdir(self.path):
      p = self._read_player(f)
      if p:
        if p.id == player_id:
          self.log.debug("Found id %s in %s, returning %s" % (player_id,f,p.name))
          return p
    
    return None
    
  def _read_player(self,filename):
    """Read a player object from a file. The file should be verified as existing before this is called."""
    self.log.debug("_read_player(): Opening %s for reading" % os.path.join(self.path,filename))
    f = open(os.path.join(self.path,filename),'r')
    with f:
      id = f.readline().strip()
      name = f.readline().strip()
      f.close()
      return Player(id,name)
    self.log.error("_read_player(): Error opening %s for reading" % os.path.join(self.path,filename))
    return None
