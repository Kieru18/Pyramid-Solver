from re import M
from classes import Board
from pytest import raises
from exceptions import SizeError


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


def test_board_init_and_size_getter():
    myboard = Board(12)
    assert myboard._size == 12
    assert myboard.size() == 12


def test_board_set_size():
    myboard = Board(12)
    assert myboard.size() == 12
    myboard.set_size(2)
    assert myboard.size() == 2


def test_board_contents_count_empty_init():
    myboard = Board(3)
    test_contents = [[{1, 2, 3}, {1, 2, 3}, {1, 2, 3}] for _ in range(3)]
    assert myboard.contents == test_contents
    assert myboard.count == {1: 0, 2: 0, 3: 0}


def test_board_str():
    myboard = Board(2)
    assert str(myboard) == "{1, 2} {1, 2} \n{1, 2} {1, 2} "


def test_board_remove_repeatitions():
    myboard = Board(2)
    myboard.contents[0][0] = {2, }
    assert myboard.contents == [[{2, }, {1, 2}], [{1, 2}, {1, 2}]]
    myboard.remove_repeatitions(0, 0)
    assert myboard.contents == [[{2, }, {1, }], [{1, }, {2, }]]


def test_board_set_biggest():
    myboard = Board(3)
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
