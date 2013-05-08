import db

class Game(object):
  def __init__(self):
    self.db = None
  
  def load_config(self):
    self.db_type = "file"
    if self.db_type is "file":
      self.db = db.FlatFileDatabase(location = "data",
                                    name = "u")
  
  def connect_db(self):
    if self.db:
      self.db.connect()
  
