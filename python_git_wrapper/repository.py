import os
import re
from typing import List, Tuple

import datetime

from python_git_wrapper.branch import Branch
from python_git_wrapper.commit import Commit
from python_git_wrapper.exceptions import RepositoryNotFoundError, RepositoryEmpty
from python_git_wrapper.git_service import GitService
from python_git_wrapper.status import Status

DELIMITER = '¡|&'


def join_flags(flags: List[Tuple[bool, str]]):
    return "".join([flag for (flagged, flag) in flags if flagged])


get_hash = lambda commits: set(commit.hash for commit in commits)


class Repository:

    _service = GitService.instance()

    def __init__(self, path: str):
        self.path = path
        self._global_args = ['-C', self.path]

    @property
    def current_branch(self) -> Branch:
        branch = self.execute(*'rev-parse --abbrev-ref HEAD'.split(' '))

        branch = branch.strip()

        if not branch:
            raise RepositoryEmpty()

        return Branch(branch)

    @property
    def branches(self) -> List[Branch]:
        branch = self.execute('branch')

        branch = [
            Branch(b.strip()) for b in branch.replace('* ', '').splitlines()
        ]

        if not branch:
            raise RepositoryEmpty()

        return branch

    @property
    def remote(self) -> List[str]:
        remotes = self.execute('remote')

        remote_cleaned = [remote for remote in remotes.splitlines()]

        return remote_cleaned

    @property
    def last_commit(self) -> Commit:
        return self.get_commit("-v")

    @classmethod
    def _create(cls, path: str):
        cls._service.run_git_command('init', path)

    @classmethod
    def build(cls,
              path: str = '.',
              create_repository: bool = False,
              create_project: bool = False):
        repository_path = os.path.join(path, '.git')

        force_create = create_repository or create_project

        if not os.path.exists(repository_path) and not force_create:
            raise RepositoryNotFoundError()
        elif create_project:
            directory_path = os.path.join(path)
            os.makedirs(directory_path)
            cls._create(directory_path)
        elif create_repository:
            cls._create(path=path)

        return cls(path=path)

    def execute(self, command: str, *args) -> str:
        response = self._service.run_git_command(*self._global_args,
                                                 *command.split(' '), *args)
        return response.stdout.decode('utf8')

    def status(self) -> Status:
        response = self.execute('status -b --porcelain=1')

        status = Status.from_porcelain_format(response)

        return status

    def add_files(self, files: List[str] = list(), all_files: bool = False):
        if all_files:
            self.execute('add -A')
        elif len(files) > 0:
            for file in files:
                self.execute('add', file)
        return self.status()

    def commit(self, message: str, add_files: bool = False) -> Status:
        if add_files:
            self.add_files(all_files=True)

        self.execute('commit -m', message)
        return self.status()

    def add_remote(self, url: str, name: str = 'origin') -> Status:
        self.execute(f'remote add {name} {url}')
        return self.status()

    def remove_remote(self, name: str = 'origin'):
        self.execute(f'remote remove {name}')
        return self.status()

    def push(self,
             remote_name: str = 'origin',
             force: bool = False,
             remote_branch: str = None,
             local_branch: str = None):

        local_branch = local_branch or self.current_branch

        flags = [(remote_branch, f':{remote_branch}'), (force, ' -f')]
        command = f'push {remote_name} {local_branch}{join_flags(flags)}'

        self.execute(command)
        return self.status()

    def pull(self,
             remote_name: str = 'origin',
             force: bool = False,
             remote_branch: str = None,
             local_branch: str = None):
        local_branch = local_branch or self.current_branch

        flags = [(remote_branch, f':{remote_branch}'), (force, ' -f')]
        command = f'pull {remote_name} {local_branch}{join_flags(flags)}'

        self.execute(command)
        return self.status()

    def revert_last_commit(self) -> Commit:
        self.execute('revert --no-edit HEAD')
        return self.last_commit

    def change_last_commit_message(self, message: str) -> Commit:
        self.execute(f'commit --amend -m', message)
        return self.last_commit

    def get_commit(self, hash: str) -> Commit:

        last_log = self.execute(
            f'show {hash} --pretty=format:"%H{DELIMITER}%an{DELIMITER}%ad{DELIMITER}%s" --date=iso -s'
        ).replace('"', '')
        chash, cauthor, cdate_time, cmessage = last_log.split(DELIMITER)

        cdate_time = datetime.datetime.strptime(cdate_time,
                                                '%Y-%m-%d %H:%M:%S %z')
        return Commit(
            hash=chash,
            author=cauthor,
            date_time=cdate_time,
            message=cmessage,
            repository=self)

    def get_commit_by_position(self, position: int) -> Commit:
        return self.get_commit(f'HEAD~{position}')

    def get_commit_parents(self, hash: str) -> List[Commit]:
        parents = self.execute(f'log --pretty=%P -n 1 {hash}').replace('"', '')
        parents = re.split(r"\s+", parents)
        parents = filter(lambda commit: commit, parents)
        return [self.get_commit(parent) for parent in parents]

    def get_commit_children(self, hash: str) -> List[Commit]:
        children = self.execute(
            f'log --reverse --pretty=%P --ancestry-path {hash}..').replace(
                '"', '')
        children = re.split(r"\s+", children)
        children = filter(
            lambda commit: commit and hash in
            get_hash(self.get_commit_parents(commit)),
            set(children))
        return [self.get_commit(child) for child in children]

    def checkout(self, destination: str) -> Status:
        self.execute(f'checkout {destination}')
        return self.status()

    def create_branch(self, name: str, move_to: bool = False) -> Branch:
        self.execute(f'branch {name}')

        if move_to:
            self.checkout(name)
        return Branch(name)

    def merge_branches(self,
                       branch_origin: Branch,
                       branch: Branch,
                       squash=False,
                       fast_forward=True,
                       new_commit=False) -> Branch:
        self.checkout(branch_origin)

        flags = [(fast_forward, " --ff-only"), (squash, " --squash"),
                 (not new_commit, " --no-commit")]
        command = f'merge{join_flags(flags)} {str(branch)}'

        self.execute(command)

        return Branch(branch_origin)

    def get_branches_by_commit(self, commit: Commit) -> List[Branch]:
        branches = self.execute(f'branch --contains {commit}')

        branches_cleaned = [
            Branch(branch.strip())
            for branch in branches.replace('* ', '').splitlines()
        ]

        return branches_cleaned
