from class_clues import Clues


def test_clues_init(mocker):
    test_data = '0 3 2 0\n0 0 0 4\n0 1 0 0\n0 0 0 0'
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=test_data))
    my_clues = Clues('foo')
    m.assert_called_once_with('foo')
    assert my_clues.clues == [['0', '3', '2', '0'], ['0', '0', '0', '4'],
                              ['0', '1', '0', '0'], ['0', '0', '0', '0']]
