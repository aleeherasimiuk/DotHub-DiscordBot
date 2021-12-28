class Field:
    name: str
    value: str
    inline: bool

    def __init__(self, name, value, inline=False):
        self.name = name
        self.value = value
        self.inline = inline

        self._validate(name)
        self._validate(value)

    def to_dict(self):
        return self.__dict__

    def _validate(self, value):
        if not value:
            raise Exception("Field values must not be empty")

    def key(self):
        return None
