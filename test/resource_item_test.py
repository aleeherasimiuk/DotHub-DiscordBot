import unittest
from main.resource_item import ResourceItem


class ResourceItemTest(unittest.TestCase):

  def test_no_title(self):
    with self.assertRaises(Exception):
      ResourceItem("", "https://google.com")

  def test_no_url(self):
    with self.assertRaises(Exception):
      ResourceItem("title", "")

  def test_invalid_url(self):
    with self.assertRaises(Exception):
      ResourceItem("title", "not_an_url")

  def test_string(self):
    item = ResourceItem("A resource", "https://google.com")
    self.assertEqual(item.build_string(), "[A resource](https://google.com)")

  def test_string_with_mini_desc(self):
    item = ResourceItem("A resource", "https://google.com", mini_description="a mini desc")
    self.assertEqual(item.build_string(), "[A resource](https://google.com) (a mini desc)")
