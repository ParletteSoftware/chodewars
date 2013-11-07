from entity import Entity
from sector import Sector

class Planet(Entity):
  def __init__(self,initial_state = {}):
    super(Planet,self).__init__(initial_state = initial_state)
    
  def __repr__(self):
    return "%s" % (self.name)
