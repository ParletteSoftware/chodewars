from cluster import Cluster
from entity import Entity

class Sector(Entity):
  def __init__(self,cluster,name):
    super(Sector,self).__init__(name,parent = cluster)
    
    #Deprecated, use self.parent instead
    self.cluster = self.parent
    
  def __repr__(self):
    return "%s-%s" % (self.parent.name,str(self.name))
  
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
