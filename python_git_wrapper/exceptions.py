class GitError(Exception):
    pass


class RepositoryException(GitError):
    pass


class RepositoryNotFoundError(RepositoryException):
    message = 'Repository not found'


class RepositoryEmpty(RepositoryException):
    message = 'Repository does not have any commits yet'

class StatusError(GitError):
    message = 'Error serializing the status'
