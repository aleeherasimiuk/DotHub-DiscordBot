from main.embed.image import Thumbnail
from main.embed.embed import Embed
from main.resource_item import ResourceItem
from typing import List


class Resource(Embed):

    def __init__(self, title, description, resources: List[ResourceItem], thumbnail_url=None, annotation=None):

        self.description = description
        self.description += "\n\n"

        for resource in resources:
            self.description += "📚 » {}\n\n".format(resource.build_string())

        if annotation:
            self.description += annotation

        thumbnail = None
        if thumbnail_url:
            thumbnail = Thumbnail(thumbnail_url)

        super().__init__("**{}**".format(title), None, self.description, None, None, '46079', thumbnail, None, None, [])

    @classmethod
    def from_dict(cls, title, description, resources, thumbnail_url=None, annotation=None):

        return cls(title, description, [ResourceItem(**item) for item in resources], thumbnail_url, annotation)
