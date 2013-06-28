from chodewars import game,player,sector

game_obj = None
return_val = None #Global object variable, assigned by action, used by main script

class Action(object):
  def __init__(self,title,action,expected_result):
    self.title = title
    self.action = action
    self.result = ""
    self.expected_result = expected_result
    self.comment = ""
  
  def run(self):
    #perform action
    global return_val #get the global var for writing
    actions = self.action.split(" ")
    if actions[0] == "create":
      if actions[1] == "game":
        global game_obj
        game_obj = game.Game()
        self.result = "return_true" if game_obj else "return_false"
      if actions[1] == "player":
        print "\tcreating player..."
        created_player = game_obj.add_player(player.Player(initial_state={'id':"email@email.com",'name':"Test Player"}))
        val = None
        if created_player.parent is None:
          print "\tcreating home sector with planet and ship..."
          val = game_obj.assign_home_sector(created_player,"Test Planet","Test Ship") if created_player else None
        self.result = "return_true" if val else "return_false"
    if actions[0] == "get":
      loaded_object = None
      if actions[1] == "player":
        if len(actions[2]) > 0:
          loaded_object = game_obj.get_player_by_id(actions[2])
          parent_object = game_obj.get_parent(loaded_object)
          print "\tloaded object %s\n\t  with parent %s and sector %s" % (loaded_object,parent_object.name,game_obj.get_parent(parent_object))
      return "return_obj" if loaded_object else "return_none"
    
    #was expected result satisfied?
    if self.result == self.expected_result:
      return True
    else:
      self.comment = "%s expected but %s received" % (self.expected_result,self.result)
      return False
  
class Test(object):
  def __init__(self,title):
    self.title = title
    self.comment = ""
    self.actions = []
  
  def add(self,action):
    self.actions.append(action)
    
  def run(self):
    for action in self.actions:
      print "Action: %s" % action.title
      if action.run():
        pass
      else:
        self.comment = "Action %s failed: %s" % (action.title,action.comment)
        return False
    return True

tests = []
good = 0 #counter
bad = 0 #counter

####################
# Test Definitions #
####################
create_game = Test("initialize the game object")
create_game.add(Action("Init Game","create game","return_true"))
tests.append(create_game)

create_player = Test("create a new player")
create_player.add(Action("Add Player","create player","return_true"))
tests.append(create_player)

load_player = Test("load a player by id")
load_player.add(Action("Load Player","get player email@email.com","return_id"))
tests.append(load_player)

#move_player = Test("move a player to a new sector")
#move_player.add(Action("Move Player","move player to an adjacent sector")

for test in tests:
  print "Test: %s" % test.title
  if test.run():
    print "...ok"
    good += 1
  else:
    print "==========error==========\n%s\n==========error==========" % test.comment
    bad += 1

print "Results: %s Total, %s Success, %s Fail" % (str(good+bad),str(good),str(bad))
