from os.path import splitext
from exceptions import WrongExtensionError


class Clues():
    def __init__(self, clues=None, filename: str = None) -> None:
        if clues is None:
            self.load_data_from_file(self, filename)
        else:
            self.clues = clues

    def load_data_from_file(self, filename: str):
        self.clues = []
        ext = splitext(filename)[:-1]
        if ext not in ['txt', 'csv']:
            raise WrongExtensionError()
        with open(filename) as file:
            for line in file:
                self.clues.append(line.strip().split())
