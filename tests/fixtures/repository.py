import os
import shutil
from random import randint

import pytest

from gyt import Repository
from gyt.commit import Commit


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

    directory_name = str(uuid4())
    os.mkdir(directory_name)

    file_name = create_random_file_in_directory(directory_name)

    repository = Repository.build(directory_name, create_repository=True)

    yield repository, file_name

    shutil.rmtree(directory_name)


@pytest.fixture
def repository_with_commits() -> Repository:
    from uuid import uuid4

    directory_name = str(uuid4())
    file_name = str(randint(0, 100000))

    os.mkdir(directory_name)
    open(os.path.join(directory_name, file_name), 'w').close()
    repository = Repository.build(directory_name, create_repository=True)
    repository.add_files(all_files=True)
    repository.commit('test')

    yield repository

    shutil.rmtree(directory_name)


def create_random_file_in_directory(directory_name: str) -> str:

    file_name = str(randint(0, 100000))

    open(os.path.join(directory_name, file_name), 'w').close()
    return file_name


def create_random_commit(repository: Repository) -> Commit:
    file_name = create_random_file_in_directory(repository.path)

    repository.add_files([file_name])
    repository.commit(file_name + "" + str(randint(0, 100000)))
    return repository.last_commit
