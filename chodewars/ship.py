from entity import Entity
from sector import Sector

class Ship(Entity):
  def __init__(self,name,sector,holds = 10):
    super(Ship,self).__init__(name,parent = sector)
    
    self.holds = holds
