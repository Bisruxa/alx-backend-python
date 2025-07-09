class DatabaseConnection:
  def __init__(self,path,mode):
    self.path = path
    self.mode= mode
  def __enter__(self):
    self.connection = open(self.path, self.mode)
    return self.connection
  def __exit__(self, exc_type, exc_value, traceback):
    self.connection.close()
with DatabaseConnection("my_file.txt", "w") as db:
  db.write("SELECT * FROM users;")