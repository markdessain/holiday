
class Record:

    def __init__(self, json):
        self.json = json

    @property
    def id(self):
        raise NotImplemented

    def key(self):
        return self.id

    def value(self):
        return self.json
