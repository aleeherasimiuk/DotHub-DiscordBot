from main.embed.author import Author
import unittest

class AuthorTest(unittest.TestCase):
    
  def test_author_from_dict(self):
    author = Author(**{
      'name': 'Pepe',
      'url': 'https://google.com',
      'icon_url': "https://google.com/image.jpg"
    })

    self.assertEquals(author.name, "@Pepe")

  def test_author_from_dict2(self):
    author = Author(**{
      'name': '@Pepe',
      'url': 'https://google.com',
      'icon_url': "https://google.com/image.jpg"
    })

    self.assertEquals(author.name, "@Pepe")


  def test_author_without_name_from_dict(self):
    with self.assertRaises(Exception) as err:
      author = Author(**{
          'url': 'https://google.com',
          'icon_url': "https://google.com/image.jpg"
      })

  def test_author_without_name(self):
    with self.assertRaises(Exception) as err:
      author = Author("", url='https://google.com', icon_url="https://google.com/image.jpg")


  def test_author_without_url(self):
    author = Author(**{
      'name': 'Pepe',
      'icon_url': "https://google.com/image.jpg"
    })

    self.assertEquals(author.url, "")

  def test_author_without_icon(self):
    author = Author(**{
      'name': 'Pepe',
      'url': "https://google.com"
    })

    self.assertEquals(author.url, "https://google.com")

  
  def test_to_dict(self):

    my_dict = {
      'name': '@Pepe',
      'url': 'https://google.com',
      'icon_url': "https://google.com/image.jpg"
    }
    author = Author(**my_dict)

    self.assertDictEqual(author.to_dict(), my_dict)


  def test_to_dict2(self):

    my_dict = {
      'name': '@Pepe',
      'url': 'https://google.com',
      'icon_url': "https://google.com/image.jpg"
    }
    author = Author("Pepe", url = "https://google.com", icon_url= "https://google.com/image.jpg")

    self.assertDictEqual(author.to_dict(), my_dict)
    
