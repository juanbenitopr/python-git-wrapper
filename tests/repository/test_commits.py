import pytest

from python_git_wrapper import GitError
from python_git_wrapper.branch import Branch
from python_git_wrapper.commit import Commit
from python_git_wrapper.repository import Repository
from tests.fixtures.repository import repository_with_commits, create_random_commit

pytest.mark.usefixtures(repository_with_commits)


def test_get_current_commit(repository_with_commits: Repository):
    commit = repository_with_commits.last_commit
    assert not commit.children
    assert not commit.parents
    new_commit = create_random_commit(repository_with_commits)
    assert set(new_commit.parents) == {commit}
    assert repository_with_commits.last_commit == new_commit


def test_merge_commit_ancestors(repository_with_commits: Repository):
    initial_commit = repository_with_commits.last_commit

    origin_branch = Branch('master')
    branch_name2 = 'test_branch2'

    branch2 = repository_with_commits.create_branch(branch_name2, move_to=True)
    random_commit_list = [
        create_random_commit(repository_with_commits) for i in range(4)
    ]

    repository_with_commits.checkout(origin_branch)
    random_commit_list2 = [
        create_random_commit(repository_with_commits) for i in range(4)
    ]

    branch_merged = repository_with_commits.merge_branches(
        origin_branch, branch2, new_commit=True, fast_forward=False)

    print(repository_with_commits.execute("l"))

    assert {random_commit_list[-1], random_commit_list2[-1]} == set(repository_with_commits.last_commit.parents)
    assert {random_commit_list[0], random_commit_list2[0]} == set(initial_commit.children)
