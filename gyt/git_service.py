import subprocess

from gyt import GitError


class GitService:

    default_path = 'git'

    _instance = None

    def __init__(self, path: str = None):
        self.path = path or GitService.default_path

    @classmethod
    def instance(cls) -> 'GitService':
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def run_git_command(cls, *args) -> subprocess.CompletedProcess:
        response = subprocess.run([cls.instance().path, *args], capture_output=True)
        cls._check_git_error(response)

        return response

    @classmethod
    def _check_git_error(cls, response: subprocess.CompletedProcess):
        try:
            response.check_returncode()
        except subprocess.CalledProcessError as error:
            raise GitError(error.stderr.decode('utf8'))

    @classmethod
    def singleton(cls, path: str = None) -> 'GitService':
        cls._instance = cls(path)
        try:
            cls._instance.run_git_command('--version')
        except FileNotFoundError:
            raise GitError(f'Git installation does not exist here: {path}')

        return cls._instance
