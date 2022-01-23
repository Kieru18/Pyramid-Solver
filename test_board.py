from board import Board
from pytest import raises
from exceptions import CluesContradicionError, SizeError, WrongDataError
from clues import Clues


def test_check_size():
    size = Board._check_size(10)
    assert size == 10
    with raises(SizeError):
        size = Board._check_size(1)


def test_check_size_negative():
    size = Board._check_size(10)
    assert size == 10
    with raises(SizeError):
        size = Board._check_size(-12)


def test_check_size_zero():
    with raises(SizeError):
        _ = Board._check_size(0)


def test_check_clues_size(mocker):
    data = ('0 '*3+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('foo')
    myboard = Board(input)
    m.assert_called_once_with('foo')
    assert myboard._check_clues_size() is True


def test_check_clues_size_3_rows(mocker):
    data = ('0 '*3+'\n')*3
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    with raises(WrongDataError):
        input = Clues('foo')
        _ = Board(input)
    m.assert_called_once_with('foo')


def test_check_clues_size_uneven_rows(mocker):
    data = ('0 '*3+'\n')*3
    data += ('0 '*2+'\n')
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    with raises(WrongDataError):
        input = Clues('foo')
        _ = Board(input)
    m.assert_called_once_with('foo')


def test_init_size_getter(mocker):
    data = ('0 '*12+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('foo')
    myboard = Board(input)
    m.assert_called_once_with('foo')
    assert myboard._size == 12
    assert myboard.size() == 12


def test_set_size(mocker):
    data = ('0 '*12+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('foo')
    myboard = Board(input)
    m.assert_called_once_with('foo')
    assert myboard.size() == 12
    myboard.set_size(2)
    assert myboard.size() == 2


def test_set_size_negative(mocker):
    data = ('0 '*12+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('foo')
    myboard = Board(input)
    m.assert_called_once_with('foo')
    assert myboard.size() == 12
    with raises(SizeError):
        myboard.set_size(-444)


def test_contents_count_empty_init(mocker):
    data = ('0 '*3+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('foo')
    myboard = Board(input)
    m.assert_called_once_with('foo')
    test_contents = [[{1, 2, 3}, {1, 2, 3}, {1, 2, 3}] for _ in range(3)]
    test_clues = [['0', '0', '0'] for _ in range(4)]
    assert myboard.contents == test_contents
    assert myboard.size() == 3
    assert myboard.count == {1: 0, 2: 0, 3: 0}
    assert myboard.clues == test_clues


def test_str(mocker):
    data = ('0 '*2+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('foo')
    myboard = Board(input)
    m.assert_called_once_with('foo')
    assert str(myboard) == "{1, 2} {1, 2} \n{1, 2} {1, 2} "


def test_make_list(mocker):
    data = ('0 '*2+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('foo')
    myboard = Board(input)
    m.assert_called_once_with('foo')
    myboard.set_biggest(0, 0)
    assert myboard.contents == [[{2, }, {1, }], [{1, }, {1, 2}]]
    myboard._make_list(0, 0, myboard.contents) == [2, 1]
    myboard._make_list(0, 1, myboard.contents) == [1, 2]
    myboard._make_list(1, 1, myboard.contents) == [2, 1]
    myboard._make_list(1, 0, myboard.contents) == [1, 2]
    myboard._make_list(2, 0, myboard.contents) == [2, 1]
    myboard._make_list(2, 1, myboard.contents) == [1, 2]
    myboard._make_list(3, 1, myboard.contents) == [2, 1]
    myboard._make_list(3, 0, myboard.contents) == [1, 2]


def test_visibility(mocker):
    test_data = '3 0 0\n0 0 0\n0 0 0\n0 1 0'
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=test_data))
    input = Clues('bar')
    m.assert_called_once_with('bar')
    myboard = Board(input)
    myboard.solve_initial_clues()
    myboard.prep_subsidiary_board()
    myboard.solve_board()
    assert myboard.visibility(0, 1, myboard.board) == 1
    assert myboard.visibility(0, 2, myboard.board) == 2
    assert myboard.visibility(3, 2, myboard.board) == 3
    assert myboard.visibility(2, 1, myboard.board) == 2
    assert myboard.visibility(1, 2, myboard.board) == 2


def test_remove_repeatitions(mocker):
    data = ('0 '*2+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    myboard.contents[0][0] = {2, }
    assert myboard.contents == [[{2, }, {1, 2}], [{1, 2}, {1, 2}]]
    myboard.remove_repeatitions(0, 0)
    assert myboard.contents == [[{2, }, {1, }], [{1, }, {1, 2}]]


def test_set_biggest(mocker):
    data = ('0 '*3+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('qux')
    myboard = Board(input)
    m.assert_called_once_with('qux')
    test_contents = [[{1, 2, 3}, {1, 2, 3}, {1, 2, 3}] for _ in range(3)]
    assert myboard.contents == test_contents
    myboard.set_biggest(2, 0)
    # 1 > X X X
    #     X X X
    #     X X X
    #     (1 pyramids seen from the left of the first row)
    result = '{3} {1, 2} {1, 2} \n{1, 2} {1, 2, 3} {1, 2, 3} '
    result += '\n{1, 2} {1, 2, 3} {1, 2, 3} '
    assert result == str(myboard)


def test_set_biggest_contradiction(mocker):
    data = ('0 '*3+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('qux')
    myboard = Board(input)
    m.assert_called_once_with('qux')
    test_contents = [[{1, 2, 3}, {1, 2, 3}, {1, 2, 3}] for _ in range(3)]
    assert myboard.contents == test_contents
    myboard.set_biggest(1, 1)
    with raises(CluesContradicionError):
        myboard.set_biggest(3, 2)


def test_fill_max(mocker):
    data = ('0 '*3+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    test_contents = [[{1, 2, 3}, {1, 2, 3}, {1, 2, 3}] for _ in range(3)]
    assert myboard.contents == test_contents
    myboard.fill_max(3, 2)
    #     X X X
    #     X X X
    #     X X X < 3
    #     (3 pyramids seen from the right of the last row)
    result = '{1, 2} {1, 3} {2, 3} \n{1, 2} {1, 3} {2, 3} '
    result += '\n{3} {2} {1} '
    assert result == str(myboard)


def test_fill_max_contradiction(mocker):
    data = ('0 '*3+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    test_contents = [[{1, 2, 3}, {1, 2, 3}, {1, 2, 3}] for _ in range(3)]
    assert myboard.contents == test_contents
    myboard.fill_max(1, 1)
    with raises(CluesContradicionError):
        myboard.fill_max(3, 2)


def test_fill(mocker):
    data = ('0 '*4+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    test_contents = [
            [set(range(1, 5)) for _ in range(4)]
            for _ in range(4)]
    assert myboard.contents == test_contents
    myboard.fill(0, 1, 3)
    result = '{1, 2, 3, 4} {1, 2} {1, 2, 3, 4} {1, 2, 3, 4} \n'
    result += '{1, 2, 3, 4} {1, 2, 3} {1, 2, 3, 4} {1, 2, 3, 4} \n'
    result += '{1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4} \n'
    result += '{1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4} {1, 2, 3, 4} '
    assert result == str(myboard)


def test_sudoku_rule(mocker):
    data = ('0 '*3+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    myboard.set_biggest(0, 0)
    myboard.set_biggest(3, 1)
    #     1
    #     X X X
    #     X X X 1
    #     X X X
    result = '{3} {1, 2} {1, 2} \n{1, 2} {1, 2} {3} '
    result += '\n{1, 2} {1, 2, 3} {1, 2} '
    assert str(myboard) == result
    myboard.sudoku_rule(3)
    result = '{3} {1, 2} {1, 2} \n{1, 2} {1, 2} {3} '
    result += '\n{1, 2} {3} {1, 2} '
    assert str(myboard) == result


def test_sudoku_rule_contradiction(mocker):
    data = ('0 '*4+'\n')*4
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    myboard.fill_max(2, 3)
    myboard.fill_max(1, 0)
    myboard.fill(3, 2, 3)
    myboard.contents[1][1] = {4, }
    with raises(CluesContradicionError):
        myboard.sudoku_rule(4)


def test_solve_initial_clues(mocker):
    data = '1 0 0 \n'
    data += ('0 '*3+'\n')*2
    data += '0 0 1 \n'
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    myboard.solve_initial_clues()
    test_contents = [[{3, }, {1, 2}, {1, 2}],
                     [{1, 2}, {3, }, {1, 2}],
                     [{1, 2}, {1, 2, }, {3, }]]
    assert myboard.contents == test_contents


def test_solve_initial_clues_wrong_clue(mocker):
    data = '9 0 0 \n'
    data += ('0 '*3+'\n')*2
    data += '0 0 1 \n'
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    with raises(WrongDataError):
        myboard.solve_initial_clues()


def test_prep_subsidiary_board(mocker):
    data = '0 0 1 0\n0 0 0 0\n0 0 1 0\n0 0 2 2'
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    myboard.solve_initial_clues()
    myboard.prep_subsidiary_board()
    test_board = [[{0, }, {0, }, {4, }, {0, }],
                  [{0, } for _ in range(4)],
                  [{4, }, {0, }, {0, }, {0, }],
                  [{0, } for _ in range(4)]]
    assert myboard.board == test_board


def test_validate(mocker):
    data = '0 0 1 0\n0 0 0 0\n0 0 1 0\n0 0 2 2'
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    myboard.solve_initial_clues()
    myboard.prep_subsidiary_board()
    assert myboard.validate_unique(0, 0, 2, myboard.board) is True


def test_validate2(mocker):
    data = '0 0 0 0\n0 0 0 4\n3 0 0 0\n0 0 0 0'
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    myboard.solve_initial_clues()
    myboard.prep_subsidiary_board()
    myboard.board[0][1] = {1, }
    assert myboard.validate_unique(0, 2, 3, myboard.board) is True


def test_verify(mocker):
    data = '0 0 1 0\n0 0 0 0\n0 0 1 0\n0 0 2 2'
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    myboard.board = [[{2, }, {3, }, {4, }, {1, }],
                     [{1, }, {2, }, {3, }, {4, }],
                     [{4, }, {1, }, {2, }, {3, }],
                     [{3, }, {4, }, {1, }, {2, }]]
    assert myboard.verify(myboard.board) is True


def test_verify_wrong(mocker):
    data = '0 0 1 0\n0 0 0 0\n0 0 1 0\n0 0 2 2'
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    m.assert_called_once_with('baz')
    myboard.board = [[{1, }, {2, }, {4, }, {3, }],
                     [{2, }, {3, }, {1, }, {4, }],
                     [{4, }, {1, }, {3, }, {2, }],
                     [{3, }, {4, }, {2, }, {1, }]]
    assert myboard.verify(myboard.board) is False


def test_solve_board(mocker):
    data = '0 0 1 0\n0 0 0 0\n0 0 1 0\n0 0 2 2'
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    test_board = [[{2, }, {3, }, {4, }, {1, }],
                  [{1, }, {2, }, {3, }, {4, }],
                  [{4, }, {1, }, {2, }, {3, }],
                  [{3, }, {4, }, {1, }, {2, }]]
    m.assert_called_once_with('baz')
    myboard.prep_subsidiary_board()
    myboard.solve_board()
    assert myboard.board == test_board


def test_solve_board_with_init_clues_reduction(mocker):
    data = '0 0 0 2 2 0 \n0 0 0 0 4 0 \n0 0 3 0 4 4 \n0 0 0 6 3 0 \n'
    m = mocker.patch('builtins.open', mocker.mock_open(read_data=data))
    input = Clues('baz')
    myboard = Board(input)
    test_board = [[{5, }, {6, }, {1, }, {4, }, {3, }, {2, }],
                  [{4, }, {1, }, {3, }, {2, }, {6, }, {5, }],
                  [{2, }, {3, }, {6, }, {1, }, {5, }, {4, }],
                  [{6, }, {5, }, {4, }, {3, }, {2, }, {1, }],
                  [{1, }, {2, }, {5, }, {6, }, {4, }, {3, }],
                  [{3, }, {4, }, {2, }, {5, }, {1, }, {6, }]]
    m.assert_called_once_with('baz')
    myboard.solve_initial_clues()
    myboard.prep_subsidiary_board()
    myboard.solve_board()
    assert myboard.board == test_board
