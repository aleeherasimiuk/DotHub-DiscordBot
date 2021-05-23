import unittest
from src.main.resource import Resource


class ResourceTest(unittest.TestCase):
  resource = Resource("Un título", "Una descripcion",
                      {
                          "Recurso #1": "https://google.com",
                          "Recurso #2": "https://google.com.ar",
                          "Recurso #3": "https://google.com.cl"
                      },
                      "https://google.es",
                      )

  def test_title(self):
    self.assertEqual("**Un título**", self.resource.title)

  def test_description(self):
    self.assertEqual("Una descripcion\n\n📚 » [Recurso #1](https://google.com)\n\n📚 » [Recurso #2](https://google.com.ar)\n\n📚 » [Recurso #3](https://google.com.cl)\n\n", self.resource.description)

  def test_thumbnail_url(self):
    self.assertEqual("https://google.es", self.resource.thumbnail_url)


  def test_color(self):
    self.assertEqual(self.resource.color, 46079)

  def test_json(self):
    dictionary = self.resource.as_dict()

    expected = {
      'title': '**Un título**',
      'color': 46079,
      'description': "Una descripcion\n\n📚 » [Recurso #1](https://google.com)\n\n📚 » [Recurso #2](https://google.com.ar)\n\n📚 » [Recurso #3](https://google.com.cl)\n\n",  

      'thumbnail': {
        'url': "https://google.es"
      },
    }

    self.assertTrue(dictionary, expected)
  
if __name__ == '__main__':
    unittest.main()