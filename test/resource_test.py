from models.resource_item import ResourceItem
from models.resource import Resource
import unittest


class ResourceTest(unittest.TestCase):
  resource_item_1 = ResourceItem("title1", "https://google.com.ar")
  resource_item_2 = ResourceItem("title2", "https://google.com.cl", mini_description="google from chile")
  resource = Resource("title", "description", [resource_item_1, resource_item_2])

  def test_title(self):
    self.assertEqual("**title**", self.resource.title)

  def test_description(self):
    self.assertEqual(self.resource.description, "description\n\n📚 » [title1](https://google.com.ar)\n\n📚 » ["
                                                "title2](https://google.com.cl) (google from chile)\n\n")

  def test_thumbnail_url(self):
    res_with_thumbnail = Resource("title", "description", [self.resource_item_1, self.resource_item_2], thumbnail_url= "https://google.com/image.jpg")
    self.assertEqual("https://google.com/image.jpg", res_with_thumbnail.thumbnail.url)

  def test_annotation(self):
    res_with_annotation = Resource("title", "description", [self.resource_item_1, self.resource_item_2], annotation= "an annotation")
    self.assertEqual(res_with_annotation.description, "description\n\n📚 » [title1](https://google.com.ar)\n\n📚 » ["
                                                      "title2](https://google.com.cl) (google from chile)\n\nan "
                                                      "annotation")

  def test_color(self):
    self.assertEqual(self.resource.color, '46079')


if __name__ == '__main__':
    unittest.main()