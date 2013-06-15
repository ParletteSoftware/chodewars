from chodewars import game,player

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
    actions = self.action.split(" ")
    if actions[0] == "create":
      global return_val #get the global var for writing
      if actions[1] == "game":
        global game_obj
        game_obj = game.Game()
        self.result = "return_true" if game_obj else "return_false"
      if actions[1] == "player":
        return_val = game_obj.add_player(player.Player("email@email.com","Test Player"))
        self.result = "return_id" if len(return_val) is 36 else "return_string"
    
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
create_player.add(Action("Add Player","create player","return_id"))
tests.append(create_player)

for test in tests:
  print "Test: %s" % test.title
  if test.run():
    print "...ok"
    good += 1
  else:
    print "==========error==========\n%s\n==========error==========" % test.comment
    bad += 1

print "Results: %s Total, %s Success, %s Fail" % (str(good+bad),str(good),str(bad))
