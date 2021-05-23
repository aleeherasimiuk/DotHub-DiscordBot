class Embed():

  title         = None
  description   = None
  fields        = []
  imageURL      = None
  color         = None
  footerText    = None
  author        = None
  thumbnail_url = None
  
  def __init__(self, title, description, imageURL, author, color, thumbnail_url, footerText):
    self.title = title
    self.description = description
    self.imageURL = imageURL
    self.author = author
    self.color = color
    self.thumbnail_url = thumbnail_url
    self.footerText = footerText

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
    self._addValueIfExists(dictionary, 'image',     'url',  self.imageURL)
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
  


