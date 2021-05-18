import json

class Config():

  webhook_url = None
  avatar_url  = None
  colab_url   = None
  username    = None


  def __init__(self, config_file):
    file = open(config_file)
    __json = json.load(file)

    self.webhook_url = __json.get('webhook_url')
    self.avatar_url = __json.get('avatar_url')
    self.username = __json.get('username')
    self.colab_url = __json.get('colab')

    file.close()


  