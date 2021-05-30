from ..webhook_message import WebhookMessage
from ..config import Config

class Youtube(WebhookMessage):


  def __init__(self, config: Config, channel_name, channel_url, title, video_url):

    content = "Hey! [@{}](<{}>) ha subido un nuevo [vídeo]({})!".format(channel_name, channel_url, video_url)
    super().__init__(config, [], content=content)