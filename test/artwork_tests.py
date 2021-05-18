import unittest
from src.main.artwork import Artwork

class TestArtwork(unittest.TestCase):
  artwork = Artwork("titulo", "https://google.com", "un_algoritmo", "https://google.com.cl", "https://google.es", "un autor")

  def test_titulo(self):
    self.assertEqual(self.artwork.title, "titulo")
  
  def test_desc(self):

    expected = "Hecho con **un_algoritmo**\nPruebalo tú en: [Google Colab](https://google.com.cl)\n\n[Ver mensaje original](https://google.com)"

    self.assertEqual(self.artwork.description, expected)

  def test_image_url(self):
    self.assertEqual(self.artwork.imageURL, "https://google.es")

  def test_author(self):
    self.assertEqual(self.artwork.author, "un autor")

  def test_color(self):
    self.assertEqual(self.artwork.color, 5570309)
  
  def test_thumbnail_url(self):
    self.assertEqual(self.artwork.thumbnailURL, None)

  def test_footer(self):
    self.assertEqual(self.artwork.footerText, None)

  def test_json(self):
    dictionary = self.artwork.as_dict()

    expected = {
      'title': 'titulo',
      'color': 5570309,
      'description': "Hecho con **un_algoritmo**\nPruebalo tú en: [Google Colab](https://google.com.cl)\n\n[Ver mensaje original](https://google.com)",  
      'author': {
        'name': 'un autor'
      },
      'image': {
        'url': "https://google.es"
      },
    }

    self.assertTrue(dictionary, expected)
  
if __name__ == '__main__':
    unittest.main()