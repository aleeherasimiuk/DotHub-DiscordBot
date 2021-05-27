from typing import Dict
from embed import Embed

class Resource(Embed):
  
  def __init__(self, title, description, resources: Dict[str, str], thumbnail_url, annotation = None):
    
    self.description = description
    self.description += "\n\n"

    for resource_title in resources.keys():
      self.description += "📚 » [{}]({})\n\n".format(resource_title, resources[resource_title])
    
    if annotation:
      self.description += annotation

    
    super().__init__("**{}**".format(title), self.description, None, None, 46079, thumbnail_url, None)