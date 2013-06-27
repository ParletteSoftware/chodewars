from entity import Entity

class Cluster(Entity):
  def __init__(self,name,x_size,y_size,dict_values = None):
    self.x = int(x_size)
    self.y = int(y_size)
    
    #This needs to be called after the cluster-specific values are set
    super(Cluster,self).__init__(name,dict_values = dict_values)
  
  def __repr__(self):
    return "%s (%s x %s)" % (self.name,self.x,self.y)
