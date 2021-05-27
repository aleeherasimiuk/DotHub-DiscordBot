from typing import List
from .author import Author
from .image import Image
from .footer import Footer
from .field import Field
class Embed():

  title         = ""
  description   = ""
  color         = ""
  timestamp     = ""
  url           = ""

  image_url     : Image
  footer        : Footer
  author        : Author
  thumbnail_url : Image
  fields        : List[Field]
  
  def __init__(self, title, url, description, image, author, color, thumbnail, footer, timestamp, fields):
    self.title         = title
    self.description   = description
    self.url           = url
    self.color         = color
    self.timestamp     = timestamp
    self.image_url     = Image(**image)
    self.author        = Author(**author)
    self.footer        = Footer(**footer)
    self.thumbnail_url = Image(**thumbnail)
    self.fields        = [Field(**field) for field in fields]


  def add_field(self, name: str, value: str):
    self.fields.append({
      'name': name,
      'value': value
    })

  def as_dict(self):
    dictionary = {}
    dictionary['title']       = self.title
    dictionary['color']       = self.color
    dictionary['description'] = self.description

    self._addValueIfExists(dictionary, 'author',    'name', self.author)
    self._addValueIfExists(dictionary, 'image',     'url',  self.image_url)
    self._addValueIfExists(dictionary, 'thumbnail', 'url',  self.thumbnail_url)
    self._addValueIfExists(dictionary, 'footer',    'text', self.footerText)

    if len(self.fields):
      dictionary['fields'] = self.fields
    
    return dictionary


  def _addValueIfExists(self, dictionary, key, internal_key, value):
    if value:
      dictionary[key] = {
        internal_key: value
      }
  



