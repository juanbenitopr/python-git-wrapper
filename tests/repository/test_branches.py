from typing import Tuple

import pytest

from gyt import GitError
from gyt.branch import Branch
from gyt.commit import Commit
from gyt.repository import Repository
from tests.fixtures.repository import repository_with_file, repository_with_commits, create_random_commit

pytest.mark.usefixtures(repository_with_file, repository_with_commits)


def test_get_current_branch(repository_with_file: Tuple[Repository, str]):
    repository, file = repository_with_file

    repository.execute('checkout -b test_branch')
    repository.add_files(all_files=True)
    repository.commit('message')

    branch = repository.current_branch

    assert branch == 'test_branch'


def test_get_branches(repository_with_file: Tuple[Repository, str]):
    from random import randint
    import os

    repository, file = repository_with_file

    repository.add_files(all_files=True)
    repository.commit('message')

    open(os.path.join(repository.path, str(randint(0, 10000))), 'w').close()

    repository.execute(*'checkout -b test_branch'.split(' '))
    repository.add_files(all_files=True)
    repository.commit('message')

    branches = repository.branches

    assert branches == ['master', 'test_branch']


def test_create_branch(repository_with_commits: Repository):
    branch_name1 = 'test_branch1'
    branch_name2 = 'test_branch2'

    branch1 = repository_with_commits.create_branch(branch_name1)

    assert branch1 == branch_name1
    assert branch1 != repository_with_commits.status().branch

    branch2 = repository_with_commits.create_branch(branch_name2, move_to=True)

    assert branch2 == branch_name2
    assert branch2 == repository_with_commits.status().branch


def test_merge_branches(repository_with_commits: Repository):
    origin_branch = Branch('master')
    branch_name2 = 'test_branch2'

    branch2 = repository_with_commits.create_branch(branch_name2, move_to=True)
    random_commit_list = [create_random_commit(repository_with_commits) for i in range(4)]

    branch_merged = repository_with_commits.merge_branches(origin_branch, branch2)

    assert branch_merged == origin_branch

    for i, random_commit in enumerate(random_commit_list):
        commit_position = len(random_commit_list) - (i + 1)
        assert random_commit.message == repository_with_commits.get_commit_by_position(commit_position).message


def test_merge_branches_with_squash(repository_with_commits: Repository):
    origin_branch = Branch('master')
    branch_name2 = 'test_branch2'

    branch2 = repository_with_commits.create_branch(branch_name2, move_to=True)
    [create_random_commit(repository_with_commits) for i in range(4)]

    branch_merged = repository_with_commits.merge_branches(origin_branch, branch2, squash=True)

    assert branch_merged == origin_branch

    with pytest.raises(GitError):
        repository_with_commits.get_commit_by_position(2)


def test_merge_branches_with_new_commit(repository_with_commits: Repository):
    origin_branch = Branch('master')
    branch_name2 = 'test_branch2'

    branch2 = repository_with_commits.create_branch(branch_name2, move_to=True)
    [create_random_commit(repository_with_commits) for i in range(4)]

    branch_merged = repository_with_commits.merge_branches(origin_branch, branch2, new_commit=True)

    assert branch_merged == origin_branch

    assert isinstance(repository_with_commits.get_commit_by_position(2), Commit)


def test_get_branch_with_commit(repository_with_commits: Repository):
    branch_name = 'test_branch2'

    repository_with_commits.create_branch(branch_name, move_to=True)
    random_commit = create_random_commit(repository_with_commits)

    branches = repository_with_commits.get_branches_by_commit(random_commit)

    assert len(branches) == 1
    assert branches[0] == 'test_branch2'
