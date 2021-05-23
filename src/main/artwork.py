from config import Config
from typing import Dict
from embed import Embed

class Artwork(Embed):

  config: Config
  made_with = None
  
  def __init__(self, title, original_message, made_with, colabURL, imageURL, author):
    description = "Hecho con **{}**\nPruebalo tú en: [Google Colab]({})\n\n[Ver mensaje original]({})".format(made_with, colabURL, original_message)
    
    super().__init__(title, description, imageURL, author, 5570309, None, None)

  @classmethod
  def from_json(self, json: Dict[str, str], colab_url, made_with):
    made_with = made_with
    colab_url = colab_url
    title = json['title']
    original_message = json['original_url']
    image_url = json['image_url']
    author = json['author']
    return Artwork(title, original_message, made_with, colab_url, image_url, author)