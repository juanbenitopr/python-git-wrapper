from typing import Tuple

import pytest

from gyt.repository import Repository
from tests.test_operation_repo import repository_with_file

pytest.mark.usefixtures(repository_with_file)


def test_get_current_branch(repository_with_file: Tuple[Repository, str]):
    repository, file = repository_with_file

    repository.execute(*'checkout -b test_branch'.split(' '))
    repository.add(all_files=True)
    repository.commit('message')

    branch = repository.current_branch

    assert branch == 'test_branch'


def test_get_branches(repository_with_file: Tuple[Repository, str]):
    from random import randint
    import os

    repository, file = repository_with_file

    repository.add(all_files=True)
    repository.commit('message')

    open(os.path.join(repository.path, str(randint(0, 10000))), 'w').close()

    repository.execute(*'checkout -b test_branch'.split(' '))
    repository.add(all_files=True)
    repository.commit('message')

    branches = repository.local_branches

    assert branches == ['master', 'test_branch']
