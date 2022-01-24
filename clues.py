from model_io import read_from_file
from typing import Union
from os import PathLike


class Clues():
    """ Representation of clues, transfoms the input """
    def __init__(self, filename: Union[str, PathLike]) -> None:
        self.load_data_from_file(filename)

    def load_data_from_file(self, filename: Union[str, PathLike]) -> None:
        with open(filename) as file:
            self.content = read_from_file(file)
