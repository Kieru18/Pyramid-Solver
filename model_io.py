from typing import Union
from os import PathLike


def read_from_file(filename: Union[str, PathLike]) -> 'list["list[str]"]':
    clues = []
    for line in filename:
        clues.append(line.strip().split())
    return clues
