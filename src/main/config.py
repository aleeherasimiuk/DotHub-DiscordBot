import json


class Config():

  webhook_url = None
  avatar_url  = None
  colab_url   = None
  username    = None

  def __init__(self, webhook_url, avatar_url, username, colab_url):
    self.webhook_url = webhook_url
    self.username    = username
    self.avatar_url  = avatar_url
    self.colab_url   = colab_url

  @classmethod
  def from_file(self, config_file):
    file = open(config_file)
    __json = json.load(file)
    file.close()
    return self.from_dict(__json)

  @classmethod
  def from_dict(self, dictionary):
    webhook_url = dictionary.get('webhook_url')
    avatar_url  = dictionary.get('avatar_url')
    username    = dictionary.get('username')
    colab_url   = dictionary.get('colab')
    return Config(webhook_url, avatar_url, username, colab_url)


  