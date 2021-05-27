import json
import time
from config import Config
from artwork import Artwork
from webhook_message import WebhookMessage


config = Config.from_file("src/res/mock_config.json")

file = open('src/res/museo.json')
museum = json.load(file)['data']

for artwork in museum:
  art = Artwork.from_json(artwork, config.colab_url, "VQGAN + CLIP")
  message = WebhookMessage(config, embeds=[art], content= "")
  message.send()
  time.sleep(10)

file.close()