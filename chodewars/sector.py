from cluster import Cluster

class Sector(object):
  def __init__(self,cluster,id):
    self.id = int(id)
    self.cluster = cluster
    
  def __repr__(self):
    return "%s-%s" % (self.cluster.name,str(self.id))
