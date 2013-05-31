from sector import Sector

class Port(object):
  def __init__(self,name,sector = None):
    self.name = name
    
    self.sector = sector
  
  def __repr__(self):
    return "%s (%s)" % (self.name,self.sector)
  
