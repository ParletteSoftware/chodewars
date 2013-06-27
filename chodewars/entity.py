from uuid import uuid4

class Entity(object):
  def __init__(self,
               name = "Entity",
               id = uuid4(),
               parent = None,
               children = [],
               dict_values = None):
    
    #If dict_values is provided, then this is a load
    if dict_values:
      for key,value in dict_values.iteritems():
        #print "%s => %s" % (str(key),str(value))
        self.__dict__[key] = value
      #print "dict is now: %s" % str(self.__dict__)
    
    #Otherwise, this is a new object creation
    else:
      #Each entity should have a unique ID
      self.id = id
      self.name = name
      self.type = self.__class__.__name__
      
      #One parent
      self.parent = parent
      #Many children
      self.children = children
      
      self.landable = False
      self.tradeable = False
      self.dockable = False
      self.scanable = False
  
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
    d['parent'] = str(d['parent'].id) if d['parent'] else None
    
    #Convert all child objects into a list of id strings
    for child in d['children']:
      d['children'][child] = str(child.id)
    return d

  #TODO: load_from_dict()?
