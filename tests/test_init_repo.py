import os

import pytest

from gyt.exceptions import RepositoryNotFoundError
from gyt.repository import Repository


class TestInitRepo:

    def test_create_repository(self, tmp_path):
        open(f'{tmp_path}/.git', 'w').close()
        repository = Repository.build(tmp_path)

        assert isinstance(repository, Repository)
        assert repository.path == tmp_path

    def test_force_create_repository_from_project(self, tmp_path):
        repository = Repository.build(tmp_path, create_repository=True)

        assert isinstance(repository, Repository)
        assert repository.path == tmp_path
        assert os.path.exists(f'{tmp_path}/.git')

    def test_create_repository_from_zero(self, tmp_path):
        new_repo = os.path.join(tmp_path, 'new_repo')
        repository = Repository.build(new_repo, create_project=True)

        assert isinstance(repository, Repository)
        assert repository.path == new_repo
        assert os.path.exists(f'{new_repo}/.git')

    def test_repo_not_found(self, tmp_path):

        with pytest.raises(RepositoryNotFoundError):
            Repository.build(tmp_path)
