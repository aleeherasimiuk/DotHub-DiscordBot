from embed import Embed


class Artwork(Embed):
  
  def __init__(self, title, description, imageURL, author):
    super.__init__(title, description, imageURL, author, None, 5570309, None, None)