import pytest

from python_git_wrapper import Repository
from tests.fixtures.repository import empty_repository

pytest.mark.usefixtures(empty_repository)


def test_add_remote(empty_repository: Repository):
    status = empty_repository.add_remote(name='test', url='https://test.com')

    assert status.branch == None
    assert empty_repository.remote == ['test']

    empty_repository.remove_remote(name='test')


def test_remove_remote(empty_repository: Repository):
    empty_repository.add_remote(name='test', url='https://test.com')
    status = empty_repository.remove_remote(name='test')

    assert status.branch == None
    assert empty_repository.remote == []


def test_remote(empty_repository: Repository):
    empty_repository.add_remote(name='test', url='https://test.com')
    empty_repository.add_remote(name='test1', url='https://test.com')

    assert empty_repository.remote == ['test', 'test1']




