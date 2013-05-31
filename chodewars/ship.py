class Ship(object):
  def __init__(self,name,holds = 10):
    self.name = name
    self.holds = holds
  
  def __repr__(self):
    return str(self.name)
    
