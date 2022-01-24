import sys
from board import Board
from clues import Clues
import argparse
from exceptions import CannotSolveError, CluesContradicionError, WrongDataError


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("input", action='store',
                        help="path to input file")
    parser.add_argument("--save", action='store',
                        help='path to output file')
    args = parser.parse_args(argv[1:])
    try:
        input = Clues(args.input)
        board = Board(input)
        board.solve_initial_clues()
        board.prep_subsidiary_board()
        if not board.solve_board():
            raise CannotSolveError
        if args.save:
            with open(args.save, 'w') as file:
                output = ''
                for row in board.board:
                    str_row = ' '.join(str(list(value)[0]) for value in row)
                    str_row += '\n'
                    output += str_row
                output = output.rstrip()
                file.write(output)
        else:
            output = ''
            for row in board.board:
                str_row = ' '.join(str(list(value)[0]) for value in row)
                str_row += '\n'
                output += str_row
            output = output.rstrip()
            print(output)
    except CluesContradicionError:
        message = 'Cannot solve - clues contradict themselves'
        if args.save:
            with open(args.save, 'w') as file:
                file.write(message)
        else:
            print(message)
    except (CannotSolveError, WrongDataError):
        message = 'Program cannot solve the board. Clues may be incorrect'
        if args.save:
            with open(args.save, 'w') as file:
                file.write(message)
        else:
            print(message)


if __name__ == "__main__":
    main(sys.argv)
