class Field:
  name : str
  value : str
  inline : bool

  def __init__(self, name, value, iniline = False):
    self.name = name
    self.value = value
    self.inline = iniline