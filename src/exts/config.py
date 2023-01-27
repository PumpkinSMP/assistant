import json


class Config:
    def __init__(self, path):
        self.path = path
        self.data = {}

    def load(self):
        with open(self.path, "r") as f:
            self.data = json.load(f)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value

    def delete(self, key):
        del self.data[key]
