from ..webhook_message import WebhookMessage
from ..config import Config

class Twitch(WebhookMessage):

  def __init__(self, config: Config, user_name, user_login, title):

    content = "Hey! [@{}](https://twitch.tv/{}) está en directo en Twitch: {}.\nNo te lo pierdas!".format(user_name, user_login, title)
    super().__init__(config, [], content=content)
