import subprocess

from gyt.exceptions import RepositoryException


def run_git_command(*args) -> subprocess.CompletedProcess:
    response = subprocess.run(['git', *args], capture_output=True)
    _check_git_error(response)

    return response


def _check_git_error(response: subprocess.CompletedProcess):
    try:
        response.check_returncode()
    except subprocess.CalledProcessError as error:
        raise RepositoryException(error.stderr.decode('utf8'))
