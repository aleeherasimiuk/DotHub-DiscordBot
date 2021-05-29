from main.embed.image import Image
import unittest


class ImageTest(unittest.TestCase):

  def test_url(self):
    image = Image(**{'url': "https://google.com/image.jpg"})
    self.assertEqual(image.url, "https://google.com/image.jpg")

  def test_invalid_url(self):
    with self.assertRaises(Exception):
      image = Image(**{'url': "https://google.com/image"})

  def test_to_dict(self):
    image = Image(**{'url': "https://google.com/image.jpg"})
    self.assertDictEqual(image.to_dict(), {'url': "https://google.com/image.jpg"})
