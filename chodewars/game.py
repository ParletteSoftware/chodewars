import logging
import db
import random
import os

from ConfigParser import ConfigParser
from collections import deque

from player import Player
from cluster import Cluster
from sector import Sector
from planet import Planet
from ship import Ship
from commodity import Commodity

class Game(object):
  def __init__(self,bigbang = False):
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
    self.commodities = list()
    self._error = None
    
    #Output a header to the log
    self.log.info("\n%s\nGame Initialized: %s\n%s" % ("_" * 20,"","_" * 20))
    
    #Finish loading the Game object
    self.load_config()
    self.connect_db()
    if bigbang:
      self.big_bang()
    else:
      self._load_clusters()
  
  def has_error(self):
    return True if self._error else False
  
  def error(self,error = None):
    if error:
      self._error = error
      return True
    e = self._error
    self._error = None
    return e
  
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
    
    #Load commodities
    commodity_config = ConfigParser()
    conf_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'commodity.conf')
    self.log.debug("About to read commodity conf file from %s" % conf_path)
    commodity_config.readfp(open(conf_path))
    self.log.debug("commodity.conf sections: %s" % commodity_config.sections())
    for section in commodity_config.sections():
      options = commodity_config.options(section)
      self.log.debug("Processing commodity section %s with options %s" % (section,options))
      if 'name' in options:
        initial_state = {'name':commodity_config.get(section,'name')}
        if 'tradeable' in options:
          initial_state['tradeable'] = commodity_config.getboolean(section,'tradeable')
        if 'transferable' in options:
          initial_state['transferable'] = commodity_config.getboolean(section,'transferable')
        if 'count' in options:
          initial_state['count'] =commodity_config.getint(section,'count')
        c = Commodity(initial_state)
        self.log.debug("Adding commodity %s to commodities list" % c)
        if c not in self.commodities:
          self.commodities.append(c)
    self.log.info("Commodity list is %s" % self.commodities)
    
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
  
  def get_parent(self,entity):
    """Return the parent object for the given entity"""
    return self.db.load_object(entity.parent) if entity.parent else None
  
  def get_children(self,entity):
    """Return a list of child objects for the given entity"""
    children = []
    for child_id in entity.children:
      child_obj = self.db.load_object(child_id)
      self.log.debug("Loaded %s as a child of %s: %s" % (child_obj.name,
                                                         entity.name,
                                                         str(child_obj.to_dict())))
      children.append(child_obj)
    self.log.debug("Loaded children for %s: %s" % (entity.name,str(children)))
    return children
  
  def assign_child(self,parent,child):
    """Assign a child to a parent object and save both objects"""
    previous_parent = self.get_parent(child)
    self.log.debug("Assigning %s as a child of %s" % (child,parent))
    if child.id in parent.children:
      self.log.debug("%s is already a child of %s" % (child,parent))
      return True
    if parent.add_child(child):
      child.parent = parent.id
      self.save_object(parent)
      self.save_object(child)
      self.log.debug("Added child %s to %s" % (child,parent))
      
      #Remove child from previous parent
      if previous_parent:
        if previous_parent.remove_child(child):
          self.save_object(previous_parent)
          self.log.debug("Removed child %s from %s" % (child,previous_parent))
          return True
        else:
          self.log.error("Error removing child %s from %s, remove_child() returned False" % (child,previous_parent))
          return False
      else:
        return True
    return False
  
  def add_player(self,player):
    if self.db and player:
      loaded_player = self.db.load_object(id=str(player.id))
      if loaded_player:
        self.log.info("Player %s already exists, but add_player was called. Nothing is changed and the existing player is being returned")
        return loaded_player
      else:
        self.log.debug("Adding player %s" % player.name)
        result = self.db.add_player(player)
        self.log.debug("add_player() returning %s" % result)
        return result
    return None
  
  def get_player_by_id(self,player_id):
    if self.db:
      self.log.debug("Retrieving player account for id %s" % player_id)
      player = self.db.load_object(player_id)
      if player: self.log.debug("Returning player %s" % str(player.__dict__))
      return player
  
  def save_object(self,entity):
    return self.db.save_object(entity)
  
  def load_object(self,name):
    """Load an object from the database."""
    obj = self.db.load_object_by_name(name)
    self.log.debug("Loaded object %s: %s" % (name,str(obj.to_dict())))
    return obj
  
  def load_object_by_id(self,id):
    obj = self.db.load_object(id)
    self.log.debug("Loaded object %s: %s" % (obj.name,str(obj.to_dict())))
    return obj
  
  def _load_clusters(self):
    """Load the clusters instance variable from the database using the list in the config."""
    for c in self.cluster_list:
      self.log.debug("Loading cluster %s" % c)
      self.clusters[c] = self.db.load_object_by_name(c)
      if self.clusters[c]:
        self.log.debug("Cluster %s has been loaded" % c)
      else:
        added_cluster = self.db.add_cluster(Cluster(initial_state={'name':c,'x':self.cluster_size,'y':self.cluster_size}))
        if added_cluster:
          self.clusters[c] = self.db.load_object(added_cluster.id)
          self.log.debug("Cluster %s did not exist, but has been added" % c)
        else:
          self.log.error("Cluster %s was not successfully loaded. This should be fixed before proceeding. See the logfile for details." % c)
    if self.clusters:
      self.log.debug("Clusters initialized: %s" % str(self.clusters))
    else:
      self.log.info("No clusters defined, check the config.")
      
  def _find_empty_sector(self):
    """Return a random empty sector."""
    #Pick a cluster
    self.log.debug("_find_empty_sector(): Choosing random cluster from %s" % str(self.clusters))
    random_cluster = self.clusters[random.choice(self.clusters.keys())]
    self.log.debug("Random cluster selected as %s" % random_cluster)
    
    empty_sector = None
    while not empty_sector:
      random_sector_name = random.randint(1,int(random_cluster.x)*int(random_cluster.y))
      random_sector = self.db.get_sector("%s-%s" % (random_cluster,random_sector_name))
      if not random_sector:
        empty_sector = Sector(initial_state={'cluster_name':random_cluster.name,'name':random_sector_name})
    self.log.info("Empty sector found, returning %s" % empty_sector)
    return empty_sector
  
  def assign_home_sector(self,player,planet_name,ship_name):
    """Find an unused sector and assign this player to it.
    
    This should only run if the player doesn't have a parent (which means they don't have a ship).'"""
    if player.parent:
      self.log.debug("assign_home_sector(): Player %s already has a parent, returning True" % player.name)
      return True
    
    home_sector = self._find_empty_sector()
    self.log.debug("assign_home_sector(): Home sector determined to be %s" % home_sector.name)
    #We call get_sector, which will create it if it doesn't exist
    home_sector = self.get_sector("%s-%s" % (home_sector.cluster_name,home_sector.name))
    if home_sector:
      #Create planet
      planet = Planet(initial_state = {'name':planet_name})
      #Add commodities
      for commodity in self.commodities:
        self.add_commodity(planet,commodity.name,commodity.count)
      
      self.log.debug("assign_home_sector(): Adding planet %s" % planet)
      self.assign_child(home_sector,planet)
      
      #Create ship
      ship = Ship(initial_state = {'name':ship_name})
      self.assign_child(home_sector,ship)
      
      #Move player to ship
      self.assign_child(ship,player)
      return True
    else:
      self.log.error("assign_home_sector(): db.add_sector() returned None, so the sector was not successfully created")
      return False
    
  def move_child(self,entity_to_move,new_parent):
    """Move an entity to a new parent."""
    
    former_parent = self.get_parent(entity_to_move)
    self.assign_child(new_parent,entity_to_move)
  
  def move_ship(self,ship,container):
    """Move the ship to another container (such as a sector or planet).
    
    Currently this only supports moving to sectors and planets."""
    
    valid_container = False
    
    if container.type == "Sector":
      # If moving from one sector to another
      if self.get_parent(ship).type in ("Sector"):
        if container in self.get_available_warps(ship = ship):
          valid_container = True
      # If moving to a sector from a planet
      if self.get_parent(ship).type in ("Planet"):
        if self.get_parent(ship) in self.get_children(container):
          valid_container = True
    # If landing on a planet
    if container.type == "Planet":
      if container in self.get_children(self.get_parent(ship)):
        valid_container = True
    
    if valid_container:
      self.log.info("Moving %s to %s" % (ship,container))
      self.assign_child(container,ship)
      return True

    self.log.info("%s was found to be an invalid entity to move to for ship %s" % (container,ship))
    return False
  
  def move_commodity(self,commodity,target,amount):
    """Move some amount of a commodity to the target entity."""
    
    #Make sure the target is valid
    valid_target = False
    if target.type in ('Ship','Planet'):
      valid_target = True
    
    if valid_target:
      self.log.debug("%s has a count of %s, request is to move %s to %s" % (commodity,
                                                                            commodity.count,
                                                                            amount,
                                                                            target))
      if int(amount) > int(self.available_holds(target)):
        self.log.error("%s is greater than the available holds on %s (currently %s)" %
                       (amount,target,self.available_holds(target)))
        self.error("%s does not have enough holds! (%s currently available)" % (target,
                                                                                self.available_holds(target)))
        return False
      if int(amount) < int(commodity.count):
        self.log.debug("%s has a count of %s, moving %s to %s" % (commodity,
                                                                  commodity.count,
                                                                  amount,
                                                                  target))
        #Moving some of a commodity
        if self.add_commodity(target,commodity.name,amount):
          commodity.count -= int(amount)
          self.save_object(commodity)
          self.log.debug("Moved %s count of %s to %s" % (amount,commodity,target))
          return True
      else:
        self.log.debug("Moving all of %s to %s" % (commodity,target))
        #Moving all of a commodity
        self.assign_child(target,commodity)
        self.log.debug("Moved all %s to %s" % (commodity,target))
        return True
    
    return False
  
  def add_commodity(self,entity,commodity_name,amount):
    """Add a commodity from self.commodities using the given commodity name."""
    for child in self.get_children(entity):
      if child.name == commodity_name:
        #commodity already exists for this entity
        child.count = int(child.count) + int(amount)
        self.save_object(child)
        return True
    
    #commodity does not exist for this entity
    #copy it from the self.commodities master list
    initial_state = self.get_commodity_by_name(commodity_name).to_dict(no_id = True)
    initial_state['count'] = int(amount)
    new_commodity = Commodity(initial_state)
    self.assign_child(entity,new_commodity)
    self.log.debug("Created a new commodity %s with amount %s for %s" % (new_commodity,new_commodity.count,entity))
    return True
  
  def get_commodity_by_name(self,commodity_name):
    """Return a commodity object from the master commodities list."""
    for commodity in self.commodities:
      if commodity.name == commodity_name:
        return commodity
    return None
  
  def available_holds(self,entity):
    """Return the number of holds available to the entity."""
    if int(entity.holds):
      if len(entity.children):
        open_holds = int(entity.holds)
        for child_id in entity.children:
          child = self.load_object_by_id(child_id)
          if child.countable:
            open_holds = int(open_holds) - int(child.count)
        return open_holds
      return int(entity.holds)
    return 0
  
  #TODO: take a sector or cluster as a parameter
  def visualize_cluster(self,player):
    """Get a visual map for the current cluster of the player."""
    #TODO: player.sector no longer exists
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
  
  def get_available_warps(self,player = None,ship = None):
    """Return a list of sector objects available for the player."""
    if not player and not ship:
      self.log.debug("get_available_warps(): Player and Ship are both None, returning empty list")
      return []
    if player and not player.sector:
      self.log.debug("get_available_warps(): Player has no sector defined, returning empty list")
      return []
    
    if player:
      self.log.info("get_available_warps(): Passing Player parameter is deprecated, pass ship instead.")
      sector = self.get_parent(self.get_parent(player)) #Use the player's ship for location
    if ship:
      sector = self.get_parent(ship)
    
    sectors = []
    if sector:
      sector_number = int(sector.name)
      self.log.debug("Building list of available warps for sector %s" % sector.to_dict())
      cluster = self.get_parent(sector)
      self.log.debug("Cluster loaded as %s" % str(cluster))
      
      self.log.debug("Calculations: %s mod %s = %s" % (sector_number,cluster.y,sector_number % cluster.y))
      
      top_row = True if sector_number <= cluster.x else False
      left_column = True if sector_number % cluster.y == 1 else False
      bottom_row = True if sector_number >= (cluster.x * cluster.y - cluster.x) else False
      right_column = True if sector_number % cluster.y == 0 else False
      
      sector_names = []
      #nw
      if not top_row and not left_column:
        sector_names.append("%s-%s" % (sector.cluster_name,(sector_number - cluster.x - 1)))
        
      #n
      if not top_row:
        sector_names.append("%s-%s" % (sector.cluster_name,(sector_number - cluster.x)))
      
      #ne
      if not top_row and not right_column:
        sector_names.append("%s-%s" % (sector.cluster_name,(sector_number - cluster.x + 1)))
      
      #e
      if not right_column:
        sector_names.append("%s-%s" % (sector.cluster_name,(sector_number + 1)))
      
      #se
      if not bottom_row and not right_column:
        sector_names.append("%s-%s" % (sector.cluster_name,(sector_number + cluster.x + 1)))
      
      #s
      if not bottom_row:
        sector_names.append("%s-%s" % (sector.cluster_name,(sector_number + cluster.x)))
      
      #sw
      if not bottom_row and not left_column:
        sector_names.append("%s-%s" % (sector.cluster_name,(sector_number + cluster.x - 1)))
      
      #w
      if not left_column:
        sector_names.append("%s-%s" % (sector.cluster_name,(sector_number - 1)))
      
      for sector_name in sector_names:
        sectors.append(self.get_sector(sector_name))
      
    return sorted(sectors, key = lambda sector: sector.name)

  def get_sector(self,sector_name):
    """Retrieve a sector object from the database. If it doesn't exist, then create it here."""
    
    loaded_sector = self.db.load_object_by_name(sector_name)
    if loaded_sector:
      return loaded_sector
    else:
      cluster_name = sector_name.split('-')[0]
      name = sector_name.split('-')[1]
      new_sector = Sector(initial_state = {'cluster_name': cluster_name,'name': name})
      cluster = self.db.load_object_by_name(cluster_name)
      self.log.debug("get_sector(): Loaded cluster as %s" % str(cluster))
      self.assign_child(cluster,new_sector)
      self.log.debug("get_sector(): Returning sector %s with parent %s" % (str(new_sector),str(new_sector.parent)))
      return new_sector
    
    return None
  
class Cache(deque):
  """Hold a cache of objects of a limited size. When the cache is full, the oldest item is removed from the left."""
  def __init__(self,size,database):
    super(Cache,self).__init__()
    self.size = size
    self.db = database
  
  def get(self,id):
    if id in self:
      return self[id]
    else:
      #Load item from database
      self.db.load()
