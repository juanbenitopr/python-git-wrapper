from typing import Union


class Branch:

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, branch: Union['Branch', str]) -> bool:
        if isinstance(branch, Branch):
            return self.name == branch.name
        else:
            return self.name == branch

    def __str__(self):
        return self.name
