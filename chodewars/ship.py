from entity import Entity
from sector import Sector

class Ship(Entity):
  def __init__(self,initial_state = {}):
    super(Ship,self).__init__(initial_state = initial_state)
    
    self.holds = initial_state['holds'] if 'holds' in initial_state else 10
