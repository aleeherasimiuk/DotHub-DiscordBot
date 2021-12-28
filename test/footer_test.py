from models.embed.footer import Footer
import unittest


class FooterTest(unittest.TestCase):

  def test_text_not_null(self):
    with self.assertRaises(Exception):
      footer = Footer(**{
        'text': '',
        'icon_url': "https://google.com/image.jpg"
      })

  def test_no_icon(self):
    footer = Footer(**{
      'text': 'text',
    })

    self.assertEqual(footer.text, 'text')

  def test_icon(self):
    footer = Footer(**{
      'text': 'texto',
      'icon_url': "https://google.com/image.jpg"
    })

    self.assertEqual(footer.icon_url, "https://google.com/image.jpg")

  def test_invalid_icon(self):
    with self.assertRaises(Exception):
      footer = Footer(**{
        'text': '',
        'icon_url': "https://google.com/image"
      })

  def test_dict(self):
    footer = Footer(
      'texto',
      icon_url="https://google.com/image.jpg"
    )

    self.assertDictEqual(footer.to_dict(), {
      'text': 'texto',
      'icon_url': "https://google.com/image.jpg"
    })
