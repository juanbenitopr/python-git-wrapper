from subprocess import CompletedProcess

import pytest

from gyt import GitError
from gyt.git_service import GitService


def test_create_git_service():
    service = GitService.singleton('/usr/local/bin/git')
    assert isinstance(service, GitService)

    service = GitService.instance()
    assert isinstance(service, GitService)


def test_create_git_service_using_wrong_path():
    with pytest.raises(GitError):
        GitService.singleton('/usr/test')


def test_run_git_command():
    GitService.singleton('/usr/local/bin/git')

    response = GitService.run_git_command('--version')

    assert isinstance(response, CompletedProcess)

    cleaned_response = response.stdout.decode('utf8').strip().split(' ')
    assert cleaned_response[-1].split('.')[0] == '2'


def test_run_git_command_using_wrong_command():
    GitService.singleton('/usr/local/bin/git')

    with pytest.raises(GitError):
        GitService.run_git_command('--v')


def test_run_git_command_without_instance():
    GitService._instance = None

    response = GitService.run_git_command('--version')

    assert isinstance(response, CompletedProcess)

    cleaned_response = response.stdout.decode('utf8').strip().split(' ')
    assert cleaned_response[-1].split('.')[0] == '2'
