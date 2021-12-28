from models.embed.embed import Embed
import unittest
import json


def _mock_webhook_message():
  # En Pycharm puede ser que este path sea ../res/mock_webhook_message.json
  file = open("res/mock_webhook_message.json")
  __json = json.load(file)
  file.close()
  return __json


class TestEmbed(unittest.TestCase):
  embed: Embed

  def setUp(self):
    self.embed = Embed.from_dict(**_mock_webhook_message())


  def test_title(self):
    self.assertEqual(self.embed.title, "embed_title")

  def test_desc(self):
    self.assertEqual(self.embed.description, "embed_description")

  def test_image_url(self):
    self.assertEqual(self.embed.image.url,
                     "https://cdn.discordapp.com/attachments/842102491859386409/843277210449608724/crystal_library.png")

  def test_author_url(self):
    self.assertEqual(self.embed.author.name, "@an_author")

  def test_color(self):
    self.assertEqual(self.embed.color, 5570309)

  def test_footer(self):
    self.assertEqual(self.embed.footer.text, "embed_footer")

  def test_fields(self):
    self.assertEqual(self.embed.fields[0].name, "field1")
    self.assertEqual(self.embed.fields[0].value, "value1")

  def test_dict(self):
    self.maxDiff = 10000
    expected = {
      "title": "embed_title",
      "color": 5570309,
      "description": "embed_description",
      "timestamp": "",
      "url": "embed_url",
      "author": {
        "name": "@an_author",
        "url": "",
        "icon_url": ""

      },
      "image": {
        "url": "https://cdn.discordapp.com/attachments/842102491859386409/843277210449608724/crystal_library.png"
      },
      "footer": {
        "text": "embed_footer",
        "icon_url": ""
      },
      "fields": [
        {
          "name": "field1",
          "value": "value1",
          "inline": False
        }
      ],
    }

    self.assertDictEqual(self.embed.to_dict(), expected)


if __name__ == '__main__':
  unittest.main()
