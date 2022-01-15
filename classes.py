from exceptions import SizeError, CannotSolveError
from CONST import sides


class Board():
    def __init__(self, size: int = 0) -> None:
        self._size = self._check_size(size)
        self.contents = [
            [set(range(1, self._size+1)) for _ in range(self.size())]
            for _ in range(self.size())]
        # representation of the board: sets of possible values

        self.count = {i: 0 for i in range(1, self.size()+1)}

    @staticmethod
    def _check_size(size):
        if size < 2:
            raise SizeError()
        else:
            return size

    def set_size(self, new_size):
        self._size = self._check_size(new_size)

    def size(self):
        return self._size
