from cluster import Cluster

class Sector(object):
  def __init__(self,cluster,id):
    self.id = int(id)
    self.cluster = cluster
    
  def __repr__(self):
    return "%s-%s" % (self.cluster.name,str(self.id))
  
  def __cmp__(self,other):
    if self.cluster == other.cluster:
      if self.id < other.id:
        return -1
      if self.id > other.id:
        return 1
      else:
        return 0
    else:
      if self.cluster < other.cluster:
        return -1
      else:
        return 1
