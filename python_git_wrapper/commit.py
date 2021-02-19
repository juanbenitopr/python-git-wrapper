import datetime


class Commit:
    def __init__(self, hash: str, message: str, date_time: datetime.datetime,
            author: str, email: str, repository: 'Repository'):
        self._hash = hash
        self.message = message
        self.datetime = date_time
        self.author = author
        self.email = email
        self._repository = repository

    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self, value):
        raise Exception(
            'There is no possible set a new hash value, instance a new commit instead'
        )

    @property
    def children(self):
        return self._repository.get_commit_children(self.hash)

    @property
    def parents(self):
        return self._repository.get_commit_parents(self.hash)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self._hash

    def __hash__(self) -> int:
        return self._hash.__hash__()

    def __eq__(self, other: 'Commit') -> bool:
        return self.hash == other.hash
