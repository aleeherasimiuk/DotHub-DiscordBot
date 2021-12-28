from models.embed.field import Field
import unittest


class FieldTest(unittest.TestCase):

  def test_by_default_false(self):
    field = Field(**{
      'name': "nombre",
      'value': 'valor'
    })

    self.assertFalse(field.inline)

  def test_empty_value(self):
    with self.assertRaises(Exception):
      field = Field(**{
        'name': "nombre",
        'value': ''
      })

  def test_empty_name(self):
    with self.assertRaises(Exception):
      field = Field(**{
        'name': "",
        'value': 'valor'
      })

  def test_dict(self):
    my_dict = {
      'name': "nombre",
      'value': 'valor',
      'inline': False,
    }
    field = Field("nombre", "valor")

    self.assertDictEqual(field.to_dict(), my_dict)
