class Cluster(object):
  def __init__(self,name,x_size,y_size):
    self.name = name
    self.x = int(x_size)
    self.y = int(y_size)
  
  def __repr__(self):
    return "%s (%s x %s)" % (self.name,self.x,self.y)
  
