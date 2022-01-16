from class_clues import Clues
from io import StringIO


def test_clues_init():
    my_clues = Clues('data.txt')
    assert my_clues.clues == [['0', '3', '0'], ['1', '0', '0'],
                              ['0', '0', '0'], ['0', '0', '0']]
