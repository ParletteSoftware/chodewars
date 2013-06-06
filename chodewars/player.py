from ship import Ship
from sector import Sector
from entity import Entity

class Player(Entity):
  """Definition for a player in the game.
  
  This is linked to a user account, which is currently a Google account."""
  
  def __init__(self,player_id,name,sector = None,ship = None):
    #player_id is the email address (unique)
    super(Player,self).__init__(name,id = player_id,parent = ship)
    
    #Deprecated - Player's ship
    self.ship = self.parent
    
    #Deprecated - Player's location (determined from the player's ship)
    self.sector = self.ship.parent
    
  def to_dict(self):
    return {"id":self.id, "name":self.name, "sector":str(self.sector), "ship":str(self.ship)}
    
