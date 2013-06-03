from sector import Sector

class Planet(object):
  def __init__(self,sector,name):
    self.sector = sector
    self.name = name
    
  def __repr__(self):
    return "%s (%s)" % (self.name,self.sector)
