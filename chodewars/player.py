from ship import Ship
from sector import Sector
from entity import Entity

class Player(Entity):
  """Definition for a player in the game.
  
  This is linked to a user account, which is currently a Google account."""
  
  def __init__(self,initial_state = {}):
    super(Player,self).__init__(initial_state = initial_state)
