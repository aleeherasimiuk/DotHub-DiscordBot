class WebhookMessage():

  webhookURL = None
  username = None
  avatarURL = None
  content = None
  embeds = []
  
  def __init__(self, webhookURL, username, avatarURL, embeds, content = ""):
    self.webhookURL = webhookURL
    self.username   = username
    self.avatarURL  = avatarURL
    self.content    = content
    self.embeds     = embeds


  def as_dict(self):
    dictionary = {}
    dictionary['username']  = self.username
    dictionary['avatarURL'] = self.avatarURL
    if self.content:
      dictionary['content'] = self.content
    if len(self.embeds):
      dictionary['embeds']  = self.embeds

    return dictionary