import json
import os


class JsonStorage:

    def __init__(self, filename):
        self.filename = filename

    def load(self):

        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except:
            return []

    def save(self, data):

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)