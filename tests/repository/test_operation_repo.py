from typing import Tuple

import pytest

from gyt.commit import Commit
from gyt.repository import Repository
from tests.fixtures.repository import repository_with_file, empty_repository, repository_with_commits

pytest.mark.usefixtures(repository_with_file, empty_repository, repository_with_commits)


def test_empty_repository_status(empty_repository: Repository):
    status = empty_repository.status()

    assert status.branch is None
    assert status.added == []
    assert status.modified == []
    assert status.untracked == []


def test_repository_status_with_changes(repository_with_file: Tuple[Repository, str]):
    repository, file = repository_with_file

    status = repository.status()

    assert status.branch is None
    assert status.added == []
    assert status.modified == []
    assert status.untracked == [file]


def test_add_file(repository_with_file: Tuple[Repository, str]):
    repository, file = repository_with_file

    status = repository.status()

    assert status.added == []
    assert status.untracked == [file]

    status = repository.add_files(files=[file])

    assert status.added == [file]
    assert status.untracked == []


def test_add_all_files(repository_with_file: Tuple[Repository, str]):
    repository, file = repository_with_file

    status = repository.status()

    assert status.added == []
    assert status.untracked == [file]

    status = repository.add_files(all_files=True)

    assert status.added == [file]
    assert status.untracked == []


def test_commit_changes(repository_with_file: Tuple[Repository, str]):
    repository, file = repository_with_file

    status = repository.commit('message', add_files=True)

    assert status['added'] == []
    assert status['untracked'] == []


def test_get_last_commit(repository_with_commits: Repository):
    commit = repository_with_commits.last_commit

    assert isinstance(commit, Commit)
    assert commit.hash
    assert commit.message
    assert commit.datetime
    assert commit.author


def test_revert_last_commit(repository_with_commits: Repository):
    commit = repository_with_commits.revert_last_commit()

    assert isinstance(commit, Commit)
    assert commit.hash
    assert commit.message
    assert commit.datetime
    assert commit.author


def test_change_last_commit_message(repository_with_commits: Repository):
    message = 'new message'
    commit = repository_with_commits.change_last_commit_message(message)

    assert isinstance(commit, Commit)
    assert commit.hash
    assert commit.message == message



