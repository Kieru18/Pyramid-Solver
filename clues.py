from model_io import read_from_file


class Clues():
    def __init__(self, filename: str = None) -> None:
        self.load_data_from_file(filename)

    def load_data_from_file(self, filename: str) -> None:
        with open(filename) as file:
            self.clues = read_from_file(file)
