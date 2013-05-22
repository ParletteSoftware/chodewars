import os
import logging
import random

from player import Player
from cluster import Cluster
from planet import Planet
from sector import Sector

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
  
  def save_object(self,obj):
    """Save a game object to the database."""
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
  
  def add_cluster(self,cluster):
    """Add a cluster to the database."""
    pass
  
  def get_cluster(self,cluster_name):
    """Retrieve a cluster."""
    return None
    
  def add_sector(self,cluster,sector):
    """Add a sector to the given cluster."""
    return None
  
  def get_sector(self,cluster,sector_id):
    """Retrieve a list of all items in a sector."""
    return None
  
  def add_planet(self,planet):
    """Save a planet objet to the database. Planet names must be unique."""
    return None
  
  def get_planet(self,planet_name):
    """Retrieve a planet from the database."""
    return None
  
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
  
  def save_object(self,obj):
    """Save a game object to the database."""
    object_class = obj.__class__.__name__
    
    if object_class == "Player":
      self._write_file(obj,"%s.player" % obj.name)
  
  def _read_file(self,filename):
    """Read an object from a file. The file should be verified as existing before this is called."""
    self.log.debug("_read_file(): Opening %s for reading" % os.path.join(self.path,filename))
    f = open(os.path.join(self.path,filename),'r')
    extension = filename.split('.')[-1]
    self.log.debug("_read_file(): Extension for %s read as %s" % (filename,extension))
    with f:
      if extension == "player":
        id = f.readline().strip()
        name = f.readline().strip()
        cluster_name = f.readline().strip()
        sector_id = f.readline().strip()
        f.close()
        cluster = self.get_cluster(cluster_name)
        self.log.debug("_read_file(): Loaded cluster %s while loading player %s" % (cluster_name,name))
        sector = self.get_sector(cluster,sector_id) if cluster else None
        self.log.debug("_read_file(): Loaded sector %s-%s while loading player %s" % (cluster_name,sector_id,name))
        return Player(id,name,sector) if sector else None
      if extension == "cluster":
        pass
      if extension == "sector":
        cluster_name = f.readline().strip()
        #This looks strange because the path for the sector has the cluster in it
        id = filename.split('/')[-1].split('.')[0]
        f.close()
        cluster = self.get_cluster(cluster_name)
        return Sector(cluster,id) if cluster else None
      if extension == "planet":
        cluster_name = f.readline().strip()
        sector_id = f.readline().strip()
        name = f.readline().strip()
        f.close()
        cluster = self.get_cluster(cluster_name)
        sector = self.get_sector(cluster,sector_id)
        return Planet(sector,name) if sector else None
    self.log.error("_read_file(): Error opening %s for reading" % os.path.join(self.path,filename))
    return None
  
  def _write_file(self,obj,filename):
    """Wrtie the player object to file, overwriting whatever is there."""
    object_class = obj.__class__.__name__
    
    if object_class == "Sector":
      #For a sector, we need to verify that the cluster dir exists before proceeding
      self.log.debug("_write_file(): Verifying that cluster dir %s exists" % obj.cluster.name)
      self._verify_cluster_dir(obj.cluster)
    
    self.log.debug("_write_file(): Opening %s for writing" % os.path.join(self.path,filename))
    f = open(os.path.join(self.path,filename),'w')
    with f:
      self.log.debug("_write_file(): obj parameter type is %s" % object_class)
      if object_class == "Player":
        f.write("%s\n" % obj.id)
        f.write("%s\n" % obj.name)
        f.write("%s\n" % obj.sector.cluster.name if obj.sector else str(None))
        f.write("%s\n" % obj.sector.id if obj.sector else str(None))
        f.close()
        return True
      if object_class == "Sector":
        f.write("%s\n" % obj.cluster.name)
        f.write("%s\n" % obj.id)
        f.close()
        return True
      if object_class == "Planet":
        f.write("%s\n" % obj.sector.cluster.name)
        f.write("%s\n" % obj.sector.id)
        f.write("%s\n" % obj.name)
        return True
    self.log.error("_write_file(): Error opening %s for writing" % os.path.join(self.path,filename))
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
        self.log.debug("get_player(): Player file %s was found, calling _read_file()" % player_file_path)
        return self._read_file("%s.player" % player_name)
      else:
        self.log.debug("get_player(): Player file %s was not found, returning None" % player_file_path)
        return None
    else:
      self.log.error("get_player(): Database does not exist, aborting...")
      return None
  
  def get_player_by_id(self,player_id):
    """Go through each .player file to find the specified id."""
    for f in os.listdir(self.path):
      if f.endswith(".player"):
        p = self._read_file(f)
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
  
  def add_cluster(self,cluster):
    """Create a directory for this cluster if it doesn't already exist. Return the created cluster."""
    if self.db_exists():
      loaded_cluster = self.get_cluster(cluster.name)
      if loaded_cluster is None:
        if self._write_cluster(cluster,"%s.cluster" % cluster.name):
          self.log.debug("add_cluster(): Cluster file %s.cluster successfully added" % cluster.name)
          #Make a directory with the cluster's name
          if self._verify_cluster_dir(cluster):
            self.log.debug("add_cluster(): cluster directory exists")
          return cluster
        else:
          self.log.error("add_cluster(): Error writing to cluster file")
          return None
      else:
        self.log.debug("add_cluster(): Cluster already exists, returning cluster %s as loaded from file" % loaded_cluster.name)
        return loaded_cluster
    else:
      self.log.error("add_cluster(): Database does not exist, aborting...")
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
      
  
  def _write_cluster(self,cluster,filename):
    """Write a cluster object to a file, overwriting what is there."""
    self.log.debug("_write_cluster(): Opening %s for writing" % os.path.join(self.path,filename))
    f = open(os.path.join(self.path,filename),'w')
    with f:
      f.write("%s\n" % cluster.name)
      f.write("%s\n" % cluster.x)
      f.write("%s\n" % cluster.y)
      f.close()
      return True
    self.log.error("_write_cluster(): Error opening %s for writing" % os.path.join(self.path,filename))
    return False
  
  def get_cluster(self,cluster_name):
    """Return a cluster if it exists, or None if it does not."""
    if self.db_exists():
      cluster_file_path = os.path.join(self.path,"%s.cluster" % cluster_name)
      if os.path.exists(cluster_file_path):
        self.log.debug("get_cluster(): Cluster file %s was found, calling _read_cluster()" % cluster_file_path)
        return self._read_cluster("%s.cluster" % cluster_name)
      else:
        self.log.debug("get_cluster(): Cluster file %s was not found, returning None" % cluster_file_path)
        return None
    else:
      self.log.error("get_cluster(): Database does not exist, aborting...")
      return None
  
  def _read_cluster(self,filename):
    """Read a cluster file into a new Cluster object."""
    self.log.debug("_read_cluster(): Opening %s for reading" % os.path.join(self.path,filename))
    f = open(os.path.join(self.path,filename),'r')
    with f:
      name = f.readline().strip()
      x = f.readline().strip()
      y = f.readline().strip()
      f.close()
      return Cluster(name,x,y)
    self.log.error("_read_cluster(): Error opening %s for reading" % os.path.join(self.path,filename))
    return None
  
  def add_sector(self,sector):
    """Add a sector to the a cluster."""
    if self.db_exists():
      loaded_sector = self.get_sector(sector.cluster,sector.id)
      if loaded_sector is None:
        sector_filename = os.path.join(sector.cluster.name,str(sector.id))
        if self._write_file(sector,"%s.sector" % sector_filename):
          self.log.debug("add_sector(): Sector file %s.sector successfully added to cluster dir %s" % (sector.id,sector.cluster.name))
          return sector
        else:
          self.log.error("add_sector(): Error writing to sector file")
          return None
      else:
        self.log.debug("add_sector(): Sector already exists, returning sector %s/%s as loaded from file" % (loaded_sector.cluster.name,loaded_sector.id))
        return loaded_sector
    else:
      self.log.error("add_sector(): Database does not exist, aborting...")
      return None
  
  def get_sector(self,cluster,sector_id):
    """Retrieve a list of all items in a sector."""
    if not cluster: return None
    if self.db_exists():
      sector_file_path = os.path.join(self.path,cluster.name,"%s.sector" % sector_id)
      if os.path.exists(sector_file_path):
        self.log.debug("get_sector(): Sector file %s was found, calling _read_file()" % sector_file_path)
        return self._read_file("%s.sector" % os.path.join(cluster.name,str(sector_id)))
      else:
        self.log.debug("get_sector(): Sector file %s was not found, returning None" % sector_file_path)
        return None
    else:
      self.log.error("get_sector(): Database does not exist, aborting...")
      return None
  
  def add_planet(self,planet):
    """Save a planet objet to the database. Planet names must be unique."""
    if self.db_exists():
      loaded_planet = self.get_planet(planet.name)
      if loaded_planet is None:
        if self._write_file(planet,"%s.planet" % planet.name):
          self.log.debug("add_planet(): Planet file %s.planet successfully added" % planet.name)
          return True
        else:
          self.log.error("add_planet(): Erro writing planet to file")
          return False
      else:
        self.log.debug("add_planet(): Planet already exists, returning False")
        return False
    else:
      self.log.debug("add_planet(): Database does not exist, aborting...")
      return False
  
  def get_planet(self,planet_name):
    """Retrieve a planet from the database."""
    if self.db_exists():
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
