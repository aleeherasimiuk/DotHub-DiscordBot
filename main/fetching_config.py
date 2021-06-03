import json
from typing import List


class FetchingConfig:
    token: str
    channel_id: str
    allowed_reactors: List[str]
    starting_point: str
    save_path: str

    def __init__(self, token, channel_id, allowed_reactors, starting_point, save_path):
        self.token = token
        self.channel_id = channel_id
        self.allowed_reactors = allowed_reactors
        self.starting_point = starting_point
        self.save_path = save_path

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            return FetchingConfig(**json.load(f))

    def change_starting_point(self, new_starting_point, path):
        self.starting_point = new_starting_point
        with open(path, 'w') as f:
            json.dump(self.__dict__, f)
