from cluster import Cluster
from entity import Entity

class Sector(Entity):
  def __init__(self,initial_state = {}):
    super(Sector,self).__init__(initial_state = initial_state)
    
    self.cluster_name = initial_state['cluster_name'] if 'cluster_name' in initial_state else ""
    
  def __repr__(self):
    return "%s-%s" % (self.cluster_name,str(self.name))
  
  def __cmp__(self,other):
    if self.parent == other.parent:
      if self.name < other.name:
        return -1
      if self.name > other.name:
        return 1
      else:
        return 0
    else:
      if self.parent < other.parent:
        return -1
      else:
        return 1
