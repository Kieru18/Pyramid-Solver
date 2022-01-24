from exceptions import (SizeError,
                        WrongDataError,
                        CluesContradicionError)
from CONST import sides, board_array
from copy import deepcopy
from clues import Clues


class Board():
    """ Representation of a board. """
    def __init__(self, clues: 'Clues' = None) -> None:
        self.clues = clues.content
        if not self._check_clues_size():
            raise WrongDataError()

        size = len(self.clues[0])
        self._size = self._check_size(size)
        self.contents = [
            [set(range(1, self._size+1)) for _ in range(self.size())]
            for _ in range(self.size())]
        self.count = {i: 0 for i in range(1, self.size()+1)}

    @staticmethod
    def _check_size(size: int) -> int:
        if size < 2:
            raise SizeError()
        else:
            return size

    def _check_clues_size(self) -> bool:
        length = len(self.clues[0])
        rows = len(self.clues) == 4
        try:
            var = all([len(
                self.clues[i]) == length for i in range(0, 4)]) and rows
        except IndexError:
            raise WrongDataError
        else:
            return var

    def set_size(self, new_size: int) -> None:
        self._size = self._check_size(new_size)

    def size(self) -> int:
        return self._size

    def __str__(self) -> str:
        output = ''
        for row in self.contents:
            for value in row:
                output += f'{str(value)} '
            output += '\n'
        return output[:-1]

    def _make_list(self, side: int,
                   index: int, array: board_array) -> 'list[int]':
        """ Creates a list of values from a given
            board-like array for easier
            constraint checks """
        my_list = []
        if sides[side] == 'up':
            for row_index in range(self.size()):
                value = list(array[row_index][index])[0]
                my_list.append(value)
        if sides[side] == 'down':
            for row_index in range(self.size()):
                value = list(array[row_index][index])[0]
                my_list.append(value)
            my_list.reverse()
        if sides[side] == 'left':
            for column_index in range(self.size()):
                value = list(array[index][column_index])[0]
                my_list.append(value)
        if sides[side] == 'right':
            for column_index in range(self.size()):
                value = list(array[index][column_index])[0]
                my_list.append(value)
            my_list.reverse()
        return my_list

    def visibility(self, side: int, index: int, array: board_array) -> int:
        """ checks how many pyramids are visible
            from given side and position """
        max = 0
        count = 0
        heights = self._make_list(side, index, array)
        for height in heights:
            if height > max:
                count += 1
                max = height
        return count

    def remove_repeatitions(self, row_index: int, column_index: int) -> None:
        """ removes any repeated numbers
            from possible values in column and row """
        values = self.contents[row_index][column_index]
        if len(values) == 1:
            values = list(values)[0]
            for index in range(self.size()):
                self.contents[row_index][index].discard(values)
                self.contents[index][column_index].discard(values)
            self.contents[row_index][column_index].add(values)

    def set_biggest(self, side: int, index: int) -> None:
        """ solves clues with a value of 1
        (fills a cell on the edge with N) """
        if sides[side] == 'up':
            row_index = 0
            column_index = index
        elif sides[side] == 'down':
            row_index = self.size()-1
            column_index = index
        elif sides[side] == 'left':
            row_index = index
            column_index = 0
        elif sides[side] == 'right':
            row_index = index
            column_index = self.size()-1
        if self.size() in self.contents[row_index][column_index]:
            self.contents[row_index][column_index] = {self.size(), }
            self.remove_repeatitions(row_index, column_index)
        else:
            raise CluesContradicionError()

    def fill_max(self, side: int, index: int) -> None:
        """ solves clues with a value of N
        (fills board with subsequent values from 1 to N) """
        nums = [i+1 for i in range(self.size())]
        if sides[side] in {'right', 'down'}:
            nums.reverse()
        if sides[side] in {'up', 'down'}:
            col_index = index
        else:
            row_index = index

        for pos, num in enumerate(nums):
            if sides[side] in {'up', 'down'}:
                row_index = pos
            else:
                col_index = pos
            if num in self.contents[row_index][col_index]:
                self.contents[row_index][col_index] = {num, }
                self.remove_repeatitions(row_index, col_index)
            else:
                raise CluesContradicionError()

    def fill(self, side: int, index: int, value: int) -> None:
        """ solves clues with a value between 1 and N
        removes posibilities which would obstruct view
        in cells closer to edge """
        # example: 3|1234|1234|1234|1234| N=4
        #   =>      |12  |123 |1234|1234|
        nums = [i for i in range(1, self.size()+1)]
        if sides[side] in {'up', 'down'}:
            col_index = index
        else:
            row_index = index

        for pos in range(value-1):
            numset = nums[-(value-1)+pos:]
            if sides[side] == 'up':
                row_index = pos
            if sides[side] == 'down':
                row_index = self.size()-pos-1
            if sides[side] == 'left':
                col_index = pos
            if sides[side] == 'right':
                col_index = self.size()-pos-1

            self.contents[row_index][col_index] = self.contents[
                    row_index][col_index].difference(numset)

    def sudoku_rule(self, value: int) -> None:
        """ fills a cell if only one value reamains
        to be used in column/row """
        column_positions = set()
        row_positions = set()
        nums = set(range(self.size()))
        valueset = {value, }
        for row_index, row in enumerate(self.contents):
            for column_index, values in enumerate(row):
                if valueset == values:
                    column_positions.add(column_index)
                    row_positions.add(row_index)

        missing_pos_row = nums.difference(row_positions)
        missing_pos_column = nums.difference(column_positions)

        if missing_pos_row and missing_pos_column:
            missing_pos_row = list(missing_pos_row)[0]
            missing_pos_column = list(missing_pos_column)[0]

            if value in self.contents[missing_pos_row][missing_pos_column]:
                self.contents[missing_pos_row][missing_pos_column] = {value, }
                self.remove_repeatitions(missing_pos_row, missing_pos_column)
            else:
                raise CluesContradicionError()

    def solve_initial_clues(self) -> None:
        """ solves initial clues - simplifies potential values
            across the board """
        for side, row in enumerate(self.clues):
            for index, value in enumerate(row):
                if value == '0':
                    continue
                elif value == str(self.size()):
                    self.fill_max(side, index)
                elif value == '1':
                    self.set_biggest(side, index)
                elif value in [str(val) for val in range(2, self.size())]:
                    self.fill(side, index, int(value))
                else:
                    raise(WrongDataError())
        for row in self.contents:
            for value in row:
                if len(value) == 1:
                    self.count[list(value)[0]] += 1

        for value in self.count:
            if self.count[value] == self.size()-1:
                self.sudoku_rule(value)

        for row_index, row in enumerate(self.contents):
            for col_index, value in enumerate(row):
                self.remove_repeatitions(row_index, col_index)

    def validate_unique(self, row_index: int, col_index: int,
                        value: int, board: board_array) -> bool:
        """ checks if a value is unique in given column and row """
        for index in range(self.size()):
            if board[row_index][index] == {value, }:
                return False
            if board[index][col_index] == {value, }:
                return False
        return True

    def prep_subsidiary_board(self) -> None:
        """ prepares auxillary board for easier backtracking """
        self.board = deepcopy(self.contents)
        for row_index, row in enumerate(self.board):
            for col_index, value in enumerate(row):
                if len(value) > 1:
                    self.board[row_index][col_index] = {0, }

    def verify(self, solution: board_array) -> bool:
        """ verifies if current full solution is correct """
        vars = []
        for side, row in enumerate(self.clues):
            for index, clue in enumerate(row):
                if int(self.clues[side][index]):
                    vars.append(self.visibility(side,
                                                index,
                                                solution) == int(clue))
        return all(vars)

    def solve_board(self) -> bool:
        """ solves the board """
        for row_index, row in enumerate(self.contents):
            for col_index, values in enumerate(row):
                if self.board[row_index][col_index] == {0, }:
                    for possible_value in values:
                        if self.validate_unique(row_index,
                                                col_index,
                                                possible_value, self.board):
                            self.board[
                                row_index][col_index] = {possible_value, }
                            if self.solve_board():
                                return True
                            else:
                                self.board[row_index][col_index] = {0, }
                    return False
        return self.verify(self.board)
