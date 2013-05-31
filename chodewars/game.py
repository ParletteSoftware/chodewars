import logging
import db
import random

from player import Player
from cluster import Cluster
from sector import Sector
from planet import Planet
from ship import Ship
from port import Port

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
    self.clusters = {}
    
    #Finish loading the Game object
    self.load_config()
    self.connect_db()
    self._load_clusters()
  
  def load_config(self):
    self.log.debug("Loading configuration")
    
    #Database Config
    self.db_type = "file"
    if self.db_type is "file":
      self.log.info('Using flat file database')
      self.db = db.FlatFileDatabase(location = "data",
                                    name = "universe")
    
    #Universe Config
    self.cluster_size = 10
    self.cluster_list = ['alpha']
    
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
  
  def _load_clusters(self):
    """Load the clusters instance variable from the database using the list in the config."""
    for c in self.cluster_list:
      self.log.debug("Loading cluster %s" % c)
      self.clusters[c] = self.db.add_cluster(Cluster(c,self.cluster_size,self.cluster_size))
      if self.clusters[c]:
        self.log.debug("Cluster %s has been loaded" % c)
      else:
        self.log.error("Cluster %s was not successfully loaded. This should be fixed before proceeding. See the logfile for details." % c)
    if self.clusters:
      self.log.debug("Clusters initialized: %s" % str(self.clusters))
    else:
      self.log.info("No clusters defined, check the config.")
      
  def _find_empty_sector(self):
    """Return a random empty sector."""
    #Pick a cluster
    random_cluster = self.clusters[random.choice(self.clusters.keys())]
    self.log.debug("Random cluster selected as %s" % random_cluster)
    
    empty_sector = None
    while not empty_sector:
      random_sector_id = random.randint(1,int(random_cluster.x)*int(random_cluster.y))
      random_sector = self.db.get_sector(random_cluster,random_sector_id)
      if not random_sector:
        empty_sector = Sector(random_cluster,random_sector_id)
    self.log.debug("Empty sector found: %s" % empty_sector)
    return empty_sector
  
  def assign_home_sector(self,player,planet_name):
    """Find an unused sector and assign this player to it."""
    home_sector = self._find_empty_sector()
    self.log.debug("assign_home_sector(): Adding sector %s" % home_sector.id)
    if self.db.add_sector(home_sector):
      planet = Planet(home_sector,planet_name)
      self.log.debug("assign_home_sector(): Adding planet %s to database" % planet)
      self.db.add_planet(planet)
      self.log.debug("assign_home_sector(): Moving player to sector %s" % home_sector.id)
      player.sector = home_sector
      self.db.save_object(player)
      return True
    else:
      self.log.error("assign_home_sector(): db.add_sector() returned None, so the sector was not successfully created")
      return False
    
  def move_player(self,player,cluster_name,sector_id):
    available_warps = self.get_available_warps(player)
    sector = self.db.get_sector(self.db.get_cluster(cluster_name),sector_id)
    if sector in available_warps:
      self.log.debug("move_player(): Move commmand is valid, moving player %s to sector %s" % (player,sector))
      player.sector = sector
    else:
      self.log.error("move_player(): Sector %s is not in the list of available warps: %s" % (sector.id,str(available_warps)))
    if self.db.save_object(player):
      self.log.debug("move_player(): Player object saved")
      return True
    else:
      self.log.error("move_player(): Player object could not be saved")
      return False
  
  def visualize_cluster(self,player):
    """Get a visual map for the current cluster of the player."""
    if player and player.sector:
      highlight_sector = player.sector
      cluster = player.sector.cluster
      
      lines = []
      for y in xrange(0,cluster.y):
        s = ""
        for x in xrange(1,cluster.x+1):
          s += "%s " % str(x + (y * cluster.y))
        lines.append(s)
      return lines
    else:
      self.log.debug("visualize_cluster(): Player has no sector, returning empty list")
      return []
  
  def get_available_warps(self,player):
    """Return a list of sectors available for the player."""
    if not player or not player.sector:
      self.log.debug("get_available_warps(): Player has no sector defined, returning empty list")
      return []
    
    sector = player.sector
    self.log.debug("Building list of available warps for sector %s" % sector)
    cluster = player.sector.cluster
    sectors = []
    
    self.log.debug("Calculations: %s mod %s = %s" % (sector.id,cluster.y,sector.id % cluster.y))
    
    top_row = True if sector.id <= cluster.x else False
    left_column = True if sector.id % cluster.y == 1 else False
    bottom_row = True if sector.id >= (cluster.x * cluster.y - cluster.x) else False
    right_column = True if sector.id % cluster.y == 0 else False
    
    #TODO: if the sector doesn't exist, then Game should create it (and add ports to some). Remove add = True
    
    #nw
    if not top_row and not left_column:
      self.log.debug("Adding Northwest sector to sectors list")
      sectors.append(self.db.get_sector(cluster,(sector.id - cluster.x - 1),add = True))
    
    #n
    if not top_row:
      self.log.debug("Adding North sector to sectors list")
      sectors.append(self.db.get_sector(cluster,(sector.id - cluster.x),add = True))
    
    #ne
    if not top_row and not right_column:
      self.log.debug("Adding Northwest sector to sectors list")
      sectors.append(self.db.get_sector(cluster,(sector.id - cluster.x + 1),add = True))
    
    #e
    if not right_column:
      self.log.debug("Adding East sector to sectors list")
      sectors.append(self.db.get_sector(cluster,(sector.id + 1),add = True))
    
    #se
    if not bottom_row and not right_column:
      self.log.debug("Adding Southeast sector to sectors list")
      sectors.append(self.db.get_sector(cluster,(sector.id + cluster.x + 1),add = True))
    
    #s
    if not bottom_row:
      self.log.debug("Adding South sector to sectors list")
      sectors.append(self.db.get_sector(cluster,(sector.id + cluster.x),add = True))
    
    #sw
    if not bottom_row and not left_column:
      self.log.debug("Adding Southwest sector to sectors list")
      sectors.append(self.db.get_sector(cluster,(sector.id + cluster.x - 1),add = True))
    
    #w
    if not left_column:
      self.log.debug("Adding West sector to sectors list")
      sectors.append(self.db.get_sector(cluster,(sector.id - 1),add = True))
    
    return sorted(sectors, key = lambda sector: sector.id)

  def build_ship(self,player,ship_name):
    if player:
      ship = Ship(ship_name)
      if self.db.add_ship(ship):
        player.ship = ship
        if self.db.save_object(player):
          self.log.debug("build_ship(): Ship created and player was updated with this ship")
          return True
        else:
          self.log.error("build_ship(): Ship created but player was unable to be saved, so this player likely is not assigned to a ship")
          return False
      else:
        self.log.error("build_ship(): db.add_ship returned False, player was not modified")
    else:
      self.log.error("build_ship(): Programming error, player cannot be None")
    
    return False
    
