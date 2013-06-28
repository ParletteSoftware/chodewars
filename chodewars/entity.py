from uuid import uuid4

class Entity(object):
  def __init__(self,initial_state = {}):
    
    """We set each value from the initial_state dictionary if it is exists, otherwise set it to default."""
    self.id = initial_state['id'] if 'id' in initial_state else uuid4()
    
    self.name = initial_state['name'] if 'name' in initial_state else "Entity"
    
    self.type = initial_state['type'] if 'type' in initial_state else self.__class__.__name__
    
    #Parent is the id of this entity's parent
    self.parent = initial_state['parent'] if 'parent' in initial_state else None
    #Children is a list of ids that belong to this entity
    self.children = initial_state['children'] if 'children' in initial_state else []
    
    self.landable = initial_state['landable'] if 'landable' in initial_state else False
    self.tradeable = initial_state['tradeable'] if 'tradeable' in initial_state else False
    self.dockable = initial_state['dockable'] if 'dockable' in initial_state else False
    self.scanable = initial_state['scanable'] if 'scanable' in initial_state else False
  
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
  
  def to_dict(self):
    """Return a dictionary of all of the values of this object (excluding parent and children).
    
    We only use parent and children ids since that could cause some very large dictionaries when
    converting a cluster to a dictionary, which would include all sectors, ships, players, and so on."""
    
    #We don't want to modify the instance's dictionary, so we make a copy first
    d = dict(self.__dict__)
    
    #Convert the id value to a string
    d['id'] = str(self.id)
    
    #Convert the parent object to an id string
    d['parent'] = str(d['parent']) if d['parent'] else None
    
    #Convert all child objects into a list of id strings
    for child in d['children']:
      d['children'][child] = str(child)
    return d
