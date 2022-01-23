from model_io import read_from_file
from io import StringIO


def test_read_from_file():
    test_data = '0 3 2 0\n0 0 0 4\n0 1 0 0\n0 0 0 0'
    data = StringIO(test_data)
    my_clues = read_from_file(data)
    assert my_clues == [['0', '3', '2', '0'], ['0', '0', '0', '4'],
                        ['0', '1', '0', '0'], ['0', '0', '0', '0']]
