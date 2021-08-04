from typing import List, Tuple

DELIMITER = '¡|&'


def join_flags(flags: List[Tuple[bool, str]]):
    return "".join([flag for (flagged, flag) in flags if flagged])


def get_hash(commits):
    return set(commit.hash for commit in commits)
