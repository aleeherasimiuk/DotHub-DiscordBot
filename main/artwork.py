from main.embed.author import Author
from main.embed.image import Image
from .embed.embed import Embed
from datetime import datetime


class Artwork(Embed):
  date = None
  original_message = None
  uploaded = False

  def __init__(self, title, original_message, image_url, author, date=datetime.now(), uploaded = False):
    description = "Hecho con **VQGAN + CLIP**\n[Ver mensaje original]({})".format(original_message)
    self.date = date
    self.original_message = original_message
    self.uploaded = uploaded

    super().__init__(title, "", description, Image(image_url), Author(author), '5570309', None, None)

  @classmethod
  def from_dict(cls, json):
    try:
      return Artwork(**json)
    except TypeError as err:
      raise Exception(
        "There was a problem parsing json. Have you made a mistake? Key failing: {}".format(cls._get_bad_keyword(err)))

  @classmethod
  def _get_bad_keyword(cls, error):
    return error.args[0].split("'")[1]
