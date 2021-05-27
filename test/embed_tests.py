from main.embed.embed import Embed
import unittest
import json

class TestEmbed(unittest.TestCase):

  embed: Embed

  def setUp(self):
    self.embed = Embed(**self._mock_webhook_message())

  def _mock_webhook_message(self):
    file = open("res/mock_webhook_message.json")
    return json.load(file)

  def test_titulo(self):
    self.assertEqual(self.embed.title, "embed_title")
  
  def test_desc(self):
    self.assertEqual(self.embed.description, "embed_description")

  def test_image_url(self):
    self.assertEqual(self.embed.image_url.url, "https://cdn.discordapp.com/attachments/842102491859386409/843277210449608724/crystal_library.png")

  def test_image_url(self):
    self.assertEqual(self.embed.author.name, "@an_author")

  def test_color(self):
    self.assertEqual(self.embed.color, 5570309)
  
  def test_thumbnail_url(self):
    self.assertEqual(self.embed.thumbnail_url.url, "")

  def test_footer(self):
    self.assertEqual(self.embed.footer.text, "embed_footer")

  def test_fields(self):
    self.assertEqual(self.embed.fields[0].name, "field1")
    self.assertEqual(self.embed.fields[0].value, "value1")
  
if __name__ == '__main__':
    unittest.main()