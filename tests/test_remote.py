import pytest

from gyt import Repository
from tests.test_operation_repo import empty_repository

pytest.mark.usefixtures(empty_repository)


def test_add_remote(empty_repository: Repository):
    status = empty_repository.add_remote(name='test', url='https://test.com')

    assert status['branch'] == 'master'
    assert empty_repository.remote == ['test']

    empty_repository.remove_remote(name='test')


def test_remove_remote(empty_repository: Repository):
    empty_repository.add_remote(name='test', url='https://test.com')
    status = empty_repository.remove_remote(name='test')

    assert status['branch'] == 'master'
    assert empty_repository.remote == []


def test_remote(empty_repository: Repository):
    empty_repository.add_remote(name='test', url='https://test.com')
    empty_repository.add_remote(name='test1', url='https://test.com')

    assert empty_repository.remote == ['test', 'test1']




