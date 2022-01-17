import sys
import argparse
from class_board import Board
from class_clues import Clues


def main(argv):
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-i', "--input",
    # help="accept input from command line",
    #                     action="store_true")
    # args = parser.parse_args()
    # if args.input:
    #     print("a")
    input = Clues("data.txt")
    size = len(input.clues[0])
    # @TODO - checking input for size corectness and cotradictions
    board = Board(size)
    board.solve_initial_clues()


if __name__ == "__main__":
    main(sys.argv)
