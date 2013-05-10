class Player(object):
  """Definition for a player in the game.
  
  This is linked to a user account, which is currently a Google account."""
  
  def __init__(self,player_id,name):
    #player_id is the email address (unique)
    self.id = player_id
    
    #The player's name (to be displayed in game)
    self.name = name
    
  
