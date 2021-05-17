class Embed():

  title       = None
  description = None
  fields      = []
  imageURL    = None
  color       = None
  footerText  = None
  author      = None
  
  def __init__(self, title, description, imageURL, author, color, thumbnailURL, footerText):
    self.title = title
    self.description = description
    self.imageURL = imageURL
    self.author = author
    self.color = color
    self.thumbnailURL = thumbnailURL
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

    self._addValueIfExists(dictionary, 'image',     'url',  self.imageURL)
    self._addValueIfExists(dictionary, 'thumbnail', 'url',  self.thumbnailURL)
    self._addValueIfExists(dictionary, 'footer',    'text', self.footerText)

    if len(self.fields):
      dictionary['fields'] = self.fields
    
    return dictionary


  def _addValueIfExists(dictionary, key, internal_key, value):
    if value:
      dictionary[key] = {
        internal_key: value
      }
  


