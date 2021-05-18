import json

class Config():

  webhook_url = None
  avatar_url  = None
  colab_url   = None
  username    = None

  def from_file(self, config_file):
    file = open(config_file)
    __json = json.load(file)
    file.close()
    return self.from_dict(__json)

  def from_dict(self, dictionary):
    self.webhook_url = dictionary.get('webhook_url')
    self.avatar_url = dictionary.get('avatar_url')
    self.username = dictionary.get('username')
    self.colab_url = dictionary.get('colab')
    return self


  