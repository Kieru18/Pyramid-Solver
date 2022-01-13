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
