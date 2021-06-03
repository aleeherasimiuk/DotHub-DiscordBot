import re


class ResourceItem:
    title = None
    url = None
    mini_description = None

    def __init__(self, title, url, mini_description=None):
        self.title = title
        self.url = url
        self.mini_description = mini_description
        self._validate_title(title)
        self._validate_url(url)

    def build_string(self):
        url = "[{}]({})".format(self.title, self.url)

        if self.mini_description:
            url += " ({})".format(self.mini_description)

        return url

    def _validate_title(self, title):
        if not title:
            raise Exception("Resource item must have a title")

        if any([symbol in title for symbol in "!\"#$%&/()=?¡\'¿\\¸+´\{\}-.,"]):
            raise Exception("Resource title must not have symbols")

    def _validate_url(self, url):
        if not url:
            raise Exception("Resource item must have an url")

        if not re.match("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", url):
            raise Exception("Resource url is not valid")
