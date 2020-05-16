import json

from collections import defaultdict
from typing import Optional

from gyt.branch import Branch


class Status:
    symbol_names = {
        '?': 'untracked',
        'M': 'modified',
        'A': 'added',
        'D': 'deleted',
        'R': 'renamed'
    }

    def __init__(self, branch:  Branch, untracked: [str] = list(), modified: [str] = list(), added: [str] = list(),
                 deleted: [str] = list(), renamed: [str] = list()):

        self.branch = branch

        self.untracked = untracked
        self.modified = modified
        self.added = added
        self.deleted = deleted
        self.renamed = renamed

    @classmethod
    def from_porcelain_format(cls, data: str) -> 'Status':
        data_lines__list = data.splitlines()

        branch = cls._get_branch_name_from_line(data_lines__list.pop(0))

        try:
            working_directory = [cls._get_working_directory_from_line(file_and_status) for file_and_status in data_lines__list]

            status = defaultdict(list)
            for git_symbol, file in working_directory:
                git_symbol_name = cls.symbol_names[git_symbol[0]]
                status[git_symbol_name].append(file)
        except Exception as e:
            print('Error getting the repository status')

        return cls(branch, **status)

    @classmethod
    def _get_branch_name_from_line(cls, line: str) -> Optional[Branch]:
        words = line.split(' ')

        if len(words) > 2:
            return None
        return Branch(words[-1])

    @classmethod
    def _get_working_directory_from_line(cls, line: str) -> [str]:
        line = line.strip()
        if '  ' in line:
            return line.split('  ')
        return line.split(' ')

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        status__dict = dict(self.__dict__)
        status__dict['branch'] = self.branch.name
        return json.dumps(status__dict)
