from entity import Entity

class Cluster(Entity):
  def __init__(self,initial_state = {}):
    super(Cluster,self).__init__(initial_state = initial_state)
    self.x = initial_state['x'] if 'x' in initial_state else 10
    self.y = initial_state['y'] if 'y' in initial_state else 10
  
  def __repr__(self):
    return "%s (%s x %s)" % (self.name,self.x,self.y)
