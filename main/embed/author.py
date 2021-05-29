class Author():
  name: str
  url: str
  icon_url: str

  def __init__(self, name, url="", icon_url=""):
    self._validate_author(name)
    self.name = self._concat_at_to_author(name)
    self.icon_url = icon_url
    self.url = url

  def _concat_at_to_author(self, author):
    if not author.startswith('@'):
      return (author[::-1] + '@')[::-1]
    return author

  def _validate_author(self, author):
    if not author:
      raise Exception("The author must contain name!")

  def to_dict(self):
    return self.__dict__

  def key(self):
    return "author"
