from entity import Entity
from sector import Sector

class Planet(Entity):
  def __init__(self,initial_state = {}):
    #Planets should be landable by default (if not already defined)
    initial_state['landable'] = initial_state['landable'] if 'landable' in initial_state else True
    
    #Planets should be scannable by default (if not already defined)
    initial_state['scanable'] = initial_state['scanable'] if 'scanable' in initial_state else True
    
    #Planets should be habitable by default (if not already defined)
    initial_state['habitable'] = initial_state['habitable'] if 'habitable' in initial_state else True
    
    #Use the Entity __init__ method to initialize this object
    super(Planet,self).__init__(initial_state = initial_state)
    
  def __repr__(self):
    return "%s" % (self.name)
