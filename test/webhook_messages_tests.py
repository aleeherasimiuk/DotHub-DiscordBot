from main.webhook_message import WebhookMessage
from main.artwork import Artwork
from main.config import Config
import unittest


class TestWebhookMessage(unittest.TestCase):
  config = Config(**{
    'webhook_url': 'https://discord.com/api/webhooks/0/0',
    'avatar_url': 'https://google.com/image.jpg',
    'username': 'username'
  })
  artwork = Artwork("title", "https://google.es", "https://google.com.cl/image.jpg", "un autor")
  message = WebhookMessage(config, [artwork, artwork], "content")

  def test_webhook_url(self):
    self.assertEqual(self.message.webhook_url, "https://discord.com/api/webhooks/0/0")

  def test_invalid_webhook_url(self):
    with self.assertRaises(Exception):
      Config("username", "https://google.com/image.jpg", "https://google.com")

  def test_username(self):
    self.assertEqual(self.message.username, "username")

  def test_avatar(self):
    self.assertEqual(self.message.avatar_url, "https://google.com/image.jpg")

  def test_embeds_len(self):
    self.assertEqual(len(self.message.embeds), 2)

  def test_embed_title(self):
    self.assertEqual(self.message.embeds[0].title, 'title')

  def test_embed_title2(self):
    self.assertEqual(self.message.embeds[1].title, 'title')

  def test_contenido(self):
    self.assertEqual(self.message.content, "content")

  def test_json(self):
    dictionary = self.message.to_dict()
    self.maxDiff = 5000

    expected = {
      'username': 'username',
      'avatar_url': "https://google.com/image.jpg",
      'content': "content",
      'embeds': [
        {
          'title': 'title',
          'color': '5570309',
          'url': "",
          'description': "Hecho con **VQGAN + CLIP**\n\n[Ver mensaje original](https://google.es)",
          'author': {
            'name': '@un autor',
            'url': "",
            'icon_url': ""
          },
          'image': {
            'url': "https://google.com.cl/image.jpg"
          },
          'timestamp': ""
        },
        {
          'title': 'title',
          'color': '5570309',
          'url': "",
          'description': "Hecho con **VQGAN + CLIP**\n\n[Ver mensaje original](https://google.es)",
          'author': {
            'name': '@un autor',
            'url': "",
            'icon_url': ""
          },
          'image': {
            'url': "https://google.com.cl/image.jpg"
          },
          'timestamp': ""
        },
      ]
    }

    self.assertDictEqual(expected, dictionary)


if __name__ == '__main__':
  unittest.main()
