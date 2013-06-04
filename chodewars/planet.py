from entity import Entity
from sector import Sector

class Planet(Entity):
  def __init__(self,sector,name):
    super(Planet,self).__init__(name,parent = sector)
    
    #Deprecated, use self.parent instead
    self.sector = self.parent
    
  def __repr__(self):
    return "%s (%s)" % (self.name,self.parent)
