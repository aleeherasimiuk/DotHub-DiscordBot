import json
from main.resource import Resource
from main.webhook_message import WebhookMessage
from main.artwork import Artwork
from main.config import Config
import time

config = Config.from_file("res/mock_config.json") # Pycharm => agregar ../

file = open('res/resources.json')
resource = json.load(file)

res = Resource.from_dict(**resource)
message = WebhookMessage(config, embeds = [res], content = "")
message.send()

file.close()