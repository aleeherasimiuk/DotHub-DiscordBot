import requests
from config import Config
from artwork import Artwork
from webhook_message import WebhookMessage
import json
import time

config = Config("config.json")

file = open('museo.json')
museum = json.load(file)['data']

def send(data, title):
  result = requests.post(config.webhook_url, json = data)

  try:
      result.raise_for_status()
  except requests.exceptions.HTTPError as err:
      print(err)
  else:
      print("Se ha añadido {} al museo de Arte.".format(title))

for artwork in museum:
  art = Artwork(artwork['title'], artwork['original_url'], 'VQGAN + Clip', config.colab_url, artwork['image_url'], artwork['author'])
  message = WebhookMessage(config, embeds=[art], content= "")
  send(message.as_dict(), artwork['title'])
  time.sleep(10)

file.close()