import requests
from src.main.config import Config
from src.main.artwork import Artwork
from src.main.webhook_message import WebhookMessage
import json
import time

config = Config("../res/config.json")

file = open('../res/museo.json')
museum = json.load(file)['data']

for artwork in museum:
  art = Artwork(artwork['title'], artwork['original_url'], 'VQGAN + Clip', config.colab_url, artwork['image_url'], artwork['author'])
  message = WebhookMessage(config, embeds=[art], content= "")
  message.send(message.as_dict())
  time.sleep(10)

file.close()