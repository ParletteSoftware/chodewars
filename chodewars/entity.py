from uuid import uuid4

class Entity(object):
  def __init__(self,
               name,
               id = uuid4(),
               parent = None,
               children = []):
    #Each entity should have a unique ID
    self.id = id
    self.name = name
    
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
  
  
