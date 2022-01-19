import sys
from class_board import Board
from class_clues import Clues
import argparse


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", action='store',
                        help="path to input file")
    args = parser.parse_args(argv[1:])
    input = Clues(args.input)
    size = len(input.clues[0])
    # @TODO - checking input for size corectness and cotradictions
    board = Board(size, clues=input.clues)
    board.solve_initial_clues()
    board.prep_subsidiary_board()
    board.solve_board()
    for row in board.board:
        print(row)


if __name__ == "__main__":
    main(sys.argv)
