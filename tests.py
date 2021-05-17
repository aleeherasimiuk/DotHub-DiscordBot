import unittest
from embed import Embed

class TestEmbed(unittest.TestCase):
  embed = Embed("titulo", "una descripcion", "https://google.com.ar", "un autor", 123456, "https://google.com", "un footer")

  def test_titulo(self):
    self.assertEqual(self.embed.title, "titulo")
  
  def test_desc(self):
    self.assertEqual(self.embed.description, "una descripcion")

  def test_image_url(self):
    self.assertEqual(self.embed.imageURL, "https://google.com.ar")

  def test_image_url(self):
    self.assertEqual(self.embed.author, "un autor")

  def test_color(self):
    self.assertEqual(self.embed.color, 123456)
  
  def test_thumbnail_url(self):
    self.assertEqual(self.embed.thumbnailURL, "https://google.com")

  def test_footer(self):
    self.assertEqual(self.embed.footerText, "un footer")

  def test_json(self):
    dictionary = self.embed.as_dict()

    expected = {
      'title': 'titulo',
      'color': 123456,
      'description': 'una descripcion',  
      'author': {
        'name': 'un autor'
      },
      'image': {
        'url': "https://google.com.ar"
      },
      'thumbnail':{
        'url': "https://google.com"
      },
      'footer': {
        'text': "un footer"
      }
    }

    self.assertTrue(dictionary, expected)
  
if __name__ == '__main__':
    unittest.main()