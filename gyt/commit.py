import datetime


class Commit:

    def __init__(self, hash: str, message: str, date_time: datetime.datetime, author: str):
        self._hash = hash
        self.message = message
        self.datetime = date_time
        self.author = author

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, value):
        raise Exception('There is no possible set a new hash value, instance a new commit instead')

    def __str__(self):
        return self._hash

    def __hash__(self) -> str:
        return self._hash

    def __eq__(self, other: 'Commit') -> bool:
        return self.hash == other.hash
