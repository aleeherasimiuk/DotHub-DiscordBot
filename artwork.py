from embed import Embed


class Artwork(Embed):
  
  def __init__(self, title, original_message, made_with, colabURL, imageURL, author):
    description = "Hecho con **{}**\n\
      Pruebalo tú en: [Google Colab]({})\n\n\
      [Ver mensaje original]({})".format(made_with, colabURL, original_message)
    
    
    super.__init__(title, description, imageURL, author, None, 5570309, None, None)
