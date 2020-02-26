class RepositoryException(Exception):
    pass


class RepositoryNotFoundError(RepositoryException):
    message = 'Repository not found'

    def __init__(self):
        pass


class RepositoryEmpty(RepositoryException):
    message = 'Repository does not have any commits yet'

    def __init__(self):
        pass
