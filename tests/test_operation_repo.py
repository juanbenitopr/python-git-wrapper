import os
import shutil
from typing import Tuple

import pytest

from repository import Repository


@pytest.fixture
def empty_repository() -> Repository:
    from uuid import uuid4
    directory_name = str(uuid4())

    os.mkdir(directory_name)
    repository = Repository.build(directory_name, create_repository=True)
    yield repository

    shutil.rmtree(directory_name)


@pytest.fixture
def repository_with_file() -> Repository:
    from uuid import uuid4
    from random import randint

    directory_name = str(uuid4())
    file_name = str(randint(0, 100000))

    os.mkdir(directory_name)
    open(os.path.join(directory_name, file_name), 'w').close()
    repository = Repository.build(directory_name, create_repository=True)

    yield repository, file_name

    shutil.rmtree(directory_name)


def test_empty_repository_status(empty_repository: Repository):
    status = empty_repository.status()

    assert status['branch'] == 'master'
    assert status['new'] == []
    assert status['modified'] == []
    assert status['untracked'] == []


def test_repository_status_with_changes(repository_with_file: Tuple[Repository, str]):
    repository, file = repository_with_file

    status = repository.status()

    assert status['branch'] == 'master'
    assert status['new'] == []
    assert status['modified'] == []
    assert status['untracked'] == [file]


def test_add_file(repository_with_file: Tuple[Repository, str]):
    repository, file = repository_with_file

    status = repository.status()

    assert status['new'] == []
    assert status['untracked'] == [file]

    status = repository.add(files=[file])

    assert status['new'] == [file]
    assert status['untracked'] == []


def test_add_all(repository_with_file: Tuple[Repository, str]):
    repository, file = repository_with_file

    status = repository.status()

    assert status['new'] == []
    assert status['untracked'] == [file]

    status = repository.add(all_files=True)

    assert status['new'] == [file]
    assert status['untracked'] == []


def test_commit_changes(repository_with_file: Tuple[Repository, str]):
    repository, file = repository_with_file

    status = repository.add(all_files=True)

    assert status['new'] == [file]
    assert status['untracked'] == []

    status = repository.commit('message')

    assert status['new'] == []
    assert status['untracked'] == []
