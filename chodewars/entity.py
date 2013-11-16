from uuid import uuid4

class Entity(object):
  def __init__(self,initial_state = {}):
    
    """We set each value from the initial_state dictionary if it is exists, otherwise set it to default."""
    self.id = initial_state['id'] if 'id' in initial_state else uuid4()
    
    self.name = initial_state['name'] if 'name' in initial_state else "Entity"
    
    self.type = initial_state['type'] if 'type' in initial_state else self.__class__.__name__
    
    #Parent is the id of this entity's parent
    self.parent = str(initial_state['parent']) if 'parent' in initial_state else None
    ##However, if parent is loaded as the string "None", we should convert it to be python None
    if self.parent == "None":
      self.parent = None
    
    #Children is a list of ids that belong to this entity
    self.children = initial_state['children'] if 'children' in initial_state else []
    
    #Attributes
    self.landable = initial_state['landable'] if 'landable' in initial_state else False
    self.tradeable = initial_state['tradeable'] if 'tradeable' in initial_state else False
    self.transferable = initial_state['transferable'] if 'transferable' in initial_state else False
    self.dockable = initial_state['dockable'] if 'dockable' in initial_state else False
    self.scanable = initial_state['scanable'] if 'scanable' in initial_state else False
    self.habitable = initial_state['habitable'] if 'habitable' in initial_state else False
    self.countable = initial_state['countable'] = initial_state['countable'] if 'countable' in initial_state else False
    
    #Variables
    if self.countable:
      self.count = initial_state['count'] = initial_state['count'] if 'count' in initial_state else 0
      self.growth_percent = initial_state['growth_percent'] = initial_state['growth_percent'] if 'growth_percent' in initial_state else 0.0
  
  def __repr__(self):
    return str(self.name)
  
  def __cmp__(self,other):
    """Default comparison is on the name."""
    if self.name == other.name:
      return 0
    if self.name < other.name:
      return -1
    else:
      return 1
  
  def to_dict(self, no_id = False):
    """Return a dictionary of all of the values of this object (excluding parent and children).
    
    We only use parent and children ids since that could cause some very large dictionaries when
    converting a cluster to a dictionary, which would include all sectors, ships, players, and so on.
    
    The no_id parameter is useful when creating a clone of this entity, such as with commodities.
    """
    
    #We don't want to modify the instance's dictionary, so we make a copy first
    d = dict(self.__dict__)
    
    #Convert the id value to a string
    d['id'] = str(self.id)
    
    #Convert the parent object to an id string
    d['parent'] = str(self.parent) if self.parent else None
    
    #Convert all child objects into a list of id strings
    #print "children: %s" % str(self.children)
    #for child in self.children:
      #d['children'].append(str(child))
    
    if no_id:
      del d['id']
    
    return d
  
  def add_child(self,child):
    """Add a child object to this entity.
    
    Returns boolean on if this was successful"""
    
    if str(child.id) in self.children:
      return True
    else:
      self.children.append(str(child.id))
      return True
    return False
  
  def remove_child(self,child):
    """Remove a child object from this entity.
    
    Returns a boolean on if it was successful."""
    
    if str(child.id) in self.children:
      self.children.remove(str(child.id))
      #Make sure it was removed
      return True if str(child.id) not in self.children else False
    else:
      print "child not found in self.children"
    return True
