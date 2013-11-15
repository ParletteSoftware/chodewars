import os
import logging
import random
import shutil
import json

from player import Player
from cluster import Cluster
from planet import Planet
from sector import Sector
from ship import Ship
from commodity import Commodity

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
    self.log.setLevel(logging.INFO)
    
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
  
  def save_object(self,obj):
    """Save a game object to the database.
    
    Returns the id of the added object."""
    return None
  
  def load_object(self,id):
    """Load an object and return it."""
    return None
  
  def load_object_by_name(self,name):
    """Load an object from the database by name.
    
    This may be slower depending on database type."""
    return None
  
  def add_player(self,player):
    """Add a player to the database."""
    return self.save_object(player)
  
  def get_player(self,player_name = None):
    """Retrieve a player account."""
    return None
  
  def get_player_by_id(self,player_id):
    """Retrieve a player account by id."""
    return load_object(player_id)
  
  def add_cluster(self,cluster):
    """Add a cluster to the database."""
    return self.save_object(cluster)
  
  def get_cluster(self,cluster_name):
    """Retrieve a cluster."""
    return None
    
  def add_sector(self,sector):
    """Add a sector to the given cluster. The cluster is pulled from the Sector object."""
    return self.save_object(sector)
  
  def get_sector(self,sector_name):
    """Retrieve a list of all items in a sector."""
    return self.load_object_by_name(sector_name)
  
  def add_planet(self,planet):
    """Save a planet objet to the database. Planet names must be unique."""
    return self.save_object(planet)
  
  def get_planet(self,planet_name):
    """Retrieve a planet from the database."""
    return None
  
  def add_ship(self,ship):
    """Add a new ship to the database."""
    return self.save_object(ship)
  
  def get_ship(self,ship_name):
    """Retrieve a ship from the database with the given name."""
    return None
  
class FlatFileDatabase(Database):
  def db_exists(self):
    if self.path:
      if os.path.exists(self.path):
        #self.log.debug("db_exists(): %s exists, returning True" % self.path)
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
          if os.path.isdir(os.path.join(self.path,f)):
            shutil.rmtree(os.path.join(self.path,f))
          else:
            os.remove(os.path.join(self.path,f))
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
  
  def save_object(self,obj):
    """Save a game object to the database."""
    self.log.debug("Saving object: %s" % str(obj))
    return obj if self._write_json(obj,str(obj.id)) else None
  
  def load_object(self,id):
    """Load an object and return it."""
    if os.path.exists(os.path.join(self.path,str(id))):
      return self._read_json(str(id))
  
  def load_object_by_name(self,name):
    """Load an object from the database by name.
    
    This is slow for this database type."""
    for f in os.listdir(self.path):
      o = self.load_object(f)
      self.log.debug("load_object() returned %s, checking it for name of %s" % (str(o),name))
      
      if o and o.name == name:
        self.log.debug("load_object_by_name(): Found object %s matching name parameter of %s" % (str(o),name))
        self.log.debug("load_object_by_name(): %s dictionary: %s" % (str(o),o.to_dict()))
        return o
      else:
        #Handle sectors
        if o and o.type == "Sector" and "%s-%s" % (o.cluster_name,o.name) == name:
          self.log.debug("load_object_by_name(): Found sector %s matching name parameter of %s" % (str(o),name))
          return o
    self.log.info("load_object_by_name(): No object found with name %s, returning None" % name)
    return None
  
  def _write_json(self,obj,filename):
    """Convert the object's dictionary into json."""
    f = open(os.path.join(self.path,str(filename)),'w')
    with f:
      self.log.debug("Attempting to JSON-ify dictionary %s" % obj.to_dict())
      s = json.dumps(obj.to_dict())
      s = s.replace("True","true").replace("False","false")
      self.log.debug("Attempting to write json %s to %s" % (s,f))
      f.write(s)
      f.close()
      self.log.info("_write_json(): Wrote %s to %s" % (s,f))
      return True
    self.log.error("_write_json(): Error opening %s for writing" % os.path.join(self.path,filename))
    return False
  
  def _read_json(self,filename):
    """Read a file's content as json to create an object."""
    self.log.debug("_read_file(): Opening %s for reading" % os.path.join(self.path,filename))
    f = open(os.path.join(self.path,filename),'r')
    with f:
      json_str = f.read()
      self.log.debug("JSON read from file as string: %s" % json_str)
      try:
        json_dict = json.loads(json_str)
        self.log.debug("JSON converted to dictionary: %s" % str(json_dict))
        #TODO: Can this be generic? To create a class from a variable?
        if json_dict['type'] == "Cluster":
          return Cluster(initial_state = json_dict)
        elif json_dict['type'] == "Sector":
          return Sector(initial_state = json_dict)
        elif json_dict['type'] == "Player":
          return Player(initial_state = json_dict)
        elif json_dict['type'] == "Planet":
          return Planet(initial_state = json_dict)
        elif json_dict['type'] == "Ship":
          return Ship(initial_state = json_dict)
        elif json_dict['type'] == "Commodity":
          return Commodity(initial_state = json_dict)
        else:
          return Entity(initial_state = json_dict)
      except TypeError,te:
        self.log.error("File %s does not appear to be valid JSON: %s" % (filename,te))

  def get_player(self,player_name):
    """Verify a player file exists and load that Player object."""
    if self.db_exists():
      self.log.debug("get_player(): Loading player %s" % player_name)
      player_file_path = os.path.join(self.path,"%s.player" % player_name)
      if os.path.exists(player_file_path):
        self.log.debug("get_player(): Player file %s was found, calling _read_file()" % player_file_path)
        return self._read_file("%s.player" % player_name)
      else:
        self.log.debug("get_player(): Player file %s was not found, returning None" % player_file_path)
        return None
    else:
      self.log.error("get_player(): Database does not exist, aborting...")
      return None
  
  def _verify_cluster_dir(self,cluster):
    """Verify if a cluster dir exists. If not, then create it. Return False if there is a problem creating the dir."""
    cluster_path = os.path.join(self.path,cluster.name)
    if os.path.exists(cluster_path): return True
    self.log.debug("Cluster directory does not exist, creating %s" % cluster_path)
    if os.makedirs(cluster_path):
      return True
    
    self.log.error("There was an error creating the cluster directory %s" % cluster_path)
    return False
        
  def get_cluster(self,cluster_name):
    """Return a cluster if it exists, or None if it does not."""
    if self.db_exists():
      self.log.debug("get_cluster(): Retrieving cluster %s" % cluster_name)
      cluster_file_path = os.path.join(self.path,"%s.cluster" % cluster_name)
      if os.path.exists(cluster_file_path):
        self.log.debug("get_cluster(): Cluster file %s was found, calling _read_file()" % cluster_file_path)
        return self._read_file("%s.cluster" % cluster_name)
      else:
        self.log.debug("get_cluster(): Cluster file %s was not found, returning None" % cluster_file_path)
        return None
    else:
      self.log.error("get_cluster(): Database does not exist, aborting...")
      return None
  
  def get_planet(self,planet_name):
    """Retrieve a planet from the database."""
    if self.db_exists():
      self.log.debug("get_planet(): Retriving planet %s" % planet_name)
      planet_file_path = os.path.join(self.path,"%s.planet" % planet_name)
      if os.path.exists(planet_file_path):
        self.log.debug("get_planet(): Planet file %s was found, calling _read_file()" % planet_file_path)
        return self._read_file("%s.planet" % planet_name)
      else:
        self.log.debug("get_planet(): Planet file %s was not found, returning None" % planet_file_path)
        return None
    else:
      self.log.error("get_planet(): Database does not exist, aborting...")
      return None

  def get_ship(self,ship_name):
    """Retrieve a ship from the database with the given name."""
    if self.db_exists():
      self.log.debug("get_ship(): Retriving ship %s" % ship_name)
      ship_file_path = os.path.join(self.path,"%s.ship" % ship_name)
      if os.path.exists(ship_file_path):
        self.log.debug("get_ship(): Ship file %s was found, calling _read_file()" % ship_file_path)
        return self._read_file("%s.ship" % ship_name)
      else:
        self.log.debug("get_ship(): Ship file %s was not found, returning None" % ship_file_path)
        return None
    else:
      self.log.error("get_ship(): Database does not exist, aborting...")
      return None
  
