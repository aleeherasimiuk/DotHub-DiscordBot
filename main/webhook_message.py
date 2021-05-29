import requests
from main.config import Config


class WebhookMessage():
  webhook_url = None
  username = None
  avatar_url = None
  content = None
  embeds = []

  def __init__(self, config: Config, embeds, content=""):
    self.webhook_url = config.webhook_url
    self.username = config.username
    self.avatar_url = config.avatar_url
    self.content = content
    self.embeds = embeds

  def to_dict(self):
    dictionary = {'username': self.username, 'avatar_url': self.avatar_url}
    if self.content:
      dictionary['content'] = self.content
    if len(self.embeds):
      dictionary['embeds'] = [embed.to_dict() for embed in self.embeds]

    return dictionary

  def send(self):
    result = requests.post(self.webhook_url, json=self.to_dict())

    try:
      result.raise_for_status()
    except requests.exceptions.HTTPError as err:
      print(err)
    else:
      print("El mensaje se ha enviado satisfactoriamente")
