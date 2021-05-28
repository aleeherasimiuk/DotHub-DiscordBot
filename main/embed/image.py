class Image:
  url : str
  def __init__(self, url = ""):
    self.url = url
    self._validate_image_url(url)

  def _validate_image_url(self, image_url):
    extensions = ['.png', '.jpg', '.jpeg']
    if image_url and not any([extension in image_url for extension in extensions]):
      raise Exception("The image url does not appear to be an image. Please try again. [{}]".format(image_url))


  def to_dict(self):
    return self.__dict__

  def key(self):
    return "image"


class Thumbnail(Image):

  def key(self):
    return "thumbnail"