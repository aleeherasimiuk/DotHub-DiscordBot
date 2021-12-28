from models.config import Config
import unittest
from models.artwork import Artwork

class TestArtwork(unittest.TestCase):
  artwork : Artwork
  artwork_json = {
    'title': 'titulo',
    'author': 'un autor',
    'image_url': 'https://google.com/image.jpg',
    'original_message': 'https://discord.com/channels/0/0/0'
  }

  def setUp(self):
    self.artwork = Artwork.from_dict(self.artwork_json)

  def test_titulo(self):
    self.assertEqual(self.artwork.title, "titulo")
  
  def test_desc(self):

    expected = "Hecho con **VQGAN + CLIP**\n[Ver mensaje original](https://discord.com/channels/0/0/0)"

    self.assertEqual(self.artwork.description, expected)

  def test_image_url(self):
    self.assertEqual(self.artwork.image.url, "https://google.com/image.jpg")

  def test_author(self):
    self.assertEqual(self.artwork.author.name, "@un autor")

  def test_color(self):
    self.assertEqual(self.artwork.color, '5570309')
  
  def test_thumbnail_url(self):
    self.assertEqual(self.artwork.thumbnail, None)

  def test_footer(self):
    self.assertEqual(self.artwork.footer, None)

  
if __name__ == '__main__':
    unittest.main()
