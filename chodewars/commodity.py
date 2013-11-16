from entity import Entity

class Commodity(Entity):
  def __init__(self,initial_state = {}):
    #Commodities should be tradeable by default (if not already defined)
    initial_state['tradeable'] = initial_state['tradeable'] if 'tradeable' in initial_state else True
    
    #Transferable means you can move this commodity at no cost
    initial_state['transferable'] = initial_state['transferable'] if 'transferable' in initial_state else False
    
    #Commodities are unique in that they are countable
    initial_state['countable'] = initial_state['countable'] if 'countable' in initial_state else True
    
    #Commodities should have a count defined
    initial_state['count'] = initial_state['count'] if 'count' in initial_state else 100
    
    #Should this commodity grow over time? (set to 0 for no growth)
    initial_state['growth_percent'] = initial_state['growth_percent'] if 'growth_percent' in initial_state else 0.0
    
    #Use the Entity __init__ method to initialize this object
    super(Commodity,self).__init__(initial_state = initial_state)
    
  def __repr__(self):
    return "%s" % (self.name)
