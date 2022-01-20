from class_clues import Clues


def test_clues_init():
    my_clues = Clues('test_data2.txt')
    assert my_clues.clues == [['0', '3', '2', '0'], ['0', '0', '0', '4'],
                              ['0', '1', '0', '0'], ['0', '0', '0', '0']]
