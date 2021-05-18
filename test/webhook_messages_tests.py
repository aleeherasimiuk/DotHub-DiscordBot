from src.main.config import Config
from src.main.artwork import Artwork
import unittest
from src.main.webhook_message import WebhookMessage

class TestWebhookMessage(unittest.TestCase):
  
  config = Config().from_dict({
    'webhook_url': 'https://google.com.ar',
    'avatar_url': 'https://google.com',
    'colab': 'https://google.com.cl',
    'username': 'Un Username'
  })
  artwork = Artwork("titulo", "https://google.com", "un_algoritmo", "https://google.com.cl", "https://google.es", "un autor")
  message = WebhookMessage(config, [artwork, artwork], "un contenido")


  def test_webhook_url(self):
    self.assertEqual(self.message.webhook_url, "https://google.com.ar")
  
  def test_username(self):
    self.assertEqual(self.message.username, "Un Username")

  def test_avatar(self):
    self.assertEqual(self.message.avatar_url, "https://google.com")

  def test_embeds_len(self):
    self.assertEqual(len(self.message.embeds), 2)

  def test_embed_title(self):
    self.assertEqual(self.message.embeds[0].title, 'titulo')

  def test_embed_title2(self):
    self.assertEqual(self.message.embeds[1].title, 'titulo')

  def test_contenido(self):
    self.assertEqual(self.message.content, "un contenido")

  def test_json(self):
    dictionary = self.message.as_dict()

    expected = {
      'username': 'Un Username',
      'avatar_url': "https://google.com",
      'content': "un contenido",  
      'embeds': [
        {
          'title': 'titulo',
          'color': 5570309,
          'description': "Hecho con **un_algoritmo**\n\
          Pruebalo tú en: [Google Colab](https://google.com.cl)\n\n\
          [Ver mensaje original](https://google.com)",  
          'author': {
            'name': 'un autor'
          },
          'image': {
            'url': "https://google.es"
          },
        },
        {
          'title': 'titulo',
          'color': 5570309,
          'description': "Hecho con **un_algoritmo**\n\
          Pruebalo tú en: [Google Colab](https://google.com.cl)\n\n\
          [Ver mensaje original](https://google.com)",  
          'author': {
            'name': 'un autor'
          },
          'image': {
            'url': "https://google.es"
          },
        }
      ]
    }

    self.assertTrue(dictionary, expected)


if __name__ == '__main__':
    unittest.main()
