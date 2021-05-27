from typing import Dict
from embed import Embed

class Artwork(Embed):
  
  def __init__(self, title, original_message, image_url, author):
    description = "Hecho con **VQGAN + CLIP**\n\n[Ver mensaje original]({})".format(original_message)
    
    super().__init__(title, description, image_url, author, 5570309, None, None)

  @classmethod
  def from_json(self, json):
    try:
      return Artwork(**json)
    except TypeError as err:
      raise Exception("There was a problem parsing json. Have you made a mistake? Key failing: {}".format(self._get_bad_keyword(err)))

  @classmethod
  def _get_bad_keyword(self, error):
    return error.args[0].split("'")[1]