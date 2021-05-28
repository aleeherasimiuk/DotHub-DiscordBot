from typing import Text


class Footer:
  text : str
  icon_url: str

  def __init__(self, text, icon_url = ""):
    self.text = text
    self.icon_url = icon_url
    self._validate_image_url(icon_url)
    self._validate_text(text)


  def _validate_image_url(self, image_url):
    extensions = ['.png', '.jpg', '.jpeg']
    if image_url and not any([extension in image_url for extension in extensions]):
      raise Exception("The icon url does not appear to be an image. Please try again. [{}]".format(image_url))

  def _validate_text(self, text):
    if not text:
      raise Exception("Text field must not be empty")

  def to_dict(self):
    return self.__dict__

  def key(self):
    return "footer"