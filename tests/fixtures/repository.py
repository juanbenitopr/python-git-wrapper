import os
import shutil

import pytest

from gyt import Repository


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


@pytest.fixture
def repository_with_commits() -> Repository:
    from uuid import uuid4
    from random import randint

    directory_name = str(uuid4())
    file_name = str(randint(0, 100000))

    os.mkdir(directory_name)
    open(os.path.join(directory_name, file_name), 'w').close()
    repository = Repository.build(directory_name, create_repository=True)
    repository.add_files(all_files=True)
    repository.commit('test')

    yield repository

    shutil.rmtree(directory_name)
