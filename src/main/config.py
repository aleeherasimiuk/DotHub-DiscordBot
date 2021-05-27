import json

class Config():

  webhook_url: str
  avatar_url : str
  username   : str

  def __init__(self, webhook_url, avatar_url, username):
    self._validate_webhook_url(webhook_url)
    self.webhook_url = webhook_url
    self.username    = username
    self.avatar_url  = avatar_url

  @classmethod
  def from_file(self, config_file):
    __json = self._open_file(config_file)
    return self.from_json(__json)

  @classmethod
  def from_json(self, json):
    try:
      return Config(**json)
    except TypeError as err:
      raise Exception("There was a problem parsing json config. Have you made a mistake? Key failing: {}".format(self._get_bad_keyword(err)))

  @classmethod
  def _open_file(self, config_file):
    try:
      file = open(config_file, "rt")
      __json = json.load(file)
      file.close()
    except FileNotFoundError as err:
      raise Exception("There was a problem reading config file: {}. Please try again and make sure the file exists. [{}]".format(config_file, err.args))

    return __json
  
  @classmethod
  def _get_bad_keyword(self, error):
    return error.args[0].split("'")[1]


  def _validate_webhook_url(self, webhook_url):
    if not webhook_url.startswith("https://discord.com/api/webhooks/"):
      raise Exception("The webhook_url is not valid.")