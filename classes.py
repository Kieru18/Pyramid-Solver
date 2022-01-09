from exceptions import SizeError


class Board():
    def __init__(self, size: int = 0) -> None:
        self._size = self._check_size(size)

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
