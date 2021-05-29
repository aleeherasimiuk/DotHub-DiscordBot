from typing import List
from .author import Author
from .image import Image, Thumbnail
from .footer import Footer
from .field import Field


class Embed:
  title = ""
  description = ""
  color = ""
  timestamp = ""
  url = ""

  image: Image
  footer: Footer
  author: Author
  thumbnail: Thumbnail
  fields: List[Field]

  def __init__(self, title, url, description, image, author, color, thumbnail, footer, timestamp="", fields=[]):
    self.title = title
    self.description = description
    self.url = url
    self.color = color
    self.timestamp = timestamp
    self.image = image
    self.author = author
    self.footer = footer
    self.thumbnail = thumbnail
    self.fields = fields

  @classmethod
  def from_dict(cls, title, url, description, image, author, color, thumbnail, footer, timestamp, fields):
    image = cls._build_if_exist(Image, image)
    author = cls._build_if_exist(Author, author)
    footer = cls._build_if_exist(Footer, footer)
    thumbnail = cls._build_if_exist(Thumbnail, thumbnail)
    fields = [Field(**field) for field in fields if field]

    return Embed(title, url, description, image, author, color, thumbnail, footer, timestamp, fields)

  @classmethod
  def _build_if_exist(cls, function, value):
    return function(**value) if value else {}

  def add_field(self, name: str, value: str):
    self.fields.append(Field(**{
      'name': name,
      'value': value
    }))

  def to_dict(self):
    dictionary = {'title': self.title, 'url': self.url, 'color': self.color, 'description': self.description,
                  'timestamp': self.timestamp}

    other_values = [self.author, self.image, self.thumbnail, self.footer]

    for value in other_values:
      self._addValueIfExists(dictionary, value)

    if self.fields:
      dictionary['fields'] = []
      for field in self.fields:
        dictionary['fields'].append(field.to_dict())

    return dictionary

  def _addValueIfExists(self, dictionary, value):
    if value:
      dictionary[value.key()] = value.to_dict()
