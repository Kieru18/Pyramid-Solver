from os.path import splitext
from exceptions import WrongExtensionError


class Clues():
    def __init__(self, filename: str = None) -> None:
        self.load_data_from_file(filename)

    def load_data_from_file(self, filename: str):
        self.clues = []
        ext = splitext(filename)
        if ext[1] not in ['.txt', '.csv']:
            raise WrongExtensionError()
        with open(filename) as file:
            for line in file:
                self.clues.append(line.strip().split())
