from exceptions import SizeError, CannotSolveError, WrongDataError
from CONST import sides
from class_clues import Clues


class Board():
    def __init__(self, size: int = 0, clues=None) -> None:
        self._size = self._check_size(size)
        self.contents = [
            [set(range(1, self._size+1)) for _ in range(self.size())]
            for _ in range(self.size())]
        # representation of the board: sets of possible values
        self.clues = clues
        self.count = {i: 0 for i in range(1, self.size()+1)}

    @staticmethod
    def _check_size(size: int) -> int:
        if size < 2:
            raise SizeError()
        else:
            return size

    def set_size(self, new_size: int):
        self._size = self._check_size(new_size)

    def size(self):
        return self._size

    def __str__(self) -> str:
        output = ''
        for row in self.contents:
            for value in row:
                output += f'{str(value)} '
            output += '\n'
        return output[:-1]

    def _make_list(self, side, index):
        my_list = []
        if sides[side] == 'up':
            for row_index in range(self.size()):
                value = list(self.contents[row_index][index])[0]
                my_list.append(value)
        if sides[side] == 'down':
            for row_index in range(self.size()):
                value = list(self.contents[row_index][index])[0]
                my_list.append(value)
            my_list.reverse()
        if sides[side] == 'left':
            for column_index in range(self.size()):
                value = list(self.contents[index][column_index])[0]
                my_list.append(value)
        if sides[side] == 'right':
            for column_index in range(self.size()):
                value = list(self.contents[index][column_index])[0]
                my_list.append(value)
            my_list.reverse()
        return my_list

    def visibility(self, side, index):
        """ checks how many pyramids are visible
        ! only intended to be used when a row/column has been
        solved or during backtracking ! """
        max = 0
        count = 0
        heights = self._make_list(side, index)
        for height in heights:
            if height > max:
                count += 1
                max = height
        return count

    def remove_repeatitions(self, row_index, column_index):
        """ removes any repeated numbers in column and row
        recursively checks row and column for new values to delete """
        values = self.contents[row_index][column_index]
        if len(values) == 1:
            values = list(values)[0]
            for index in range(self.size()):
                self.contents[row_index][index].discard(values)
                self.contents[index][column_index].discard(values)
                self.remove_repeatitions(row_index, index)
                self.remove_repeatitions(index, column_index)
            self.contents[row_index][column_index].add(values)

    def set_biggest(self, side, index):
        """ solves clues with a value of 1
        (fills a cell on the edge with N) """
        if sides[side] == 'up':
            row_index = 0
            column_index = index
        if sides[side] == 'down':
            row_index = self.size()-1
            column_index = index
        if sides[side] == 'left':
            row_index = index
            column_index = 0
        if sides[side] == 'right':
            row_index = index
            column_index = self.size()-1
        self.contents[row_index][column_index] = {self.size(), }
        self.remove_repeatitions(row_index, column_index)

    def fill_max(self, side, index):
        """ solves clues with a value of N
        (fills board with subsequent values from 1 to N) """
        # @FIXME
        # code fragmentarisation
        if sides[side] == 'up':
            for row_index in range(self.size()):
                self.contents[row_index][index] = {row_index+1, }
                self.remove_repeatitions(row_index, index)
        if sides[side] == 'down':
            for row_index in range(self.size()):
                self.contents[row_index][index] = {self.size()-row_index, }
                self.remove_repeatitions(row_index, index)
        if sides[side] == 'left':
            for col_index in range(self.size()):
                self.contents[index][col_index] = {col_index+1, }
                self.remove_repeatitions(index, col_index)
        if sides[side] == 'right':
            for col_index in range(self.size()):
                self.contents[index][col_index] = {self.size()-col_index, }
                self.remove_repeatitions(index, col_index)

    def fill(self, side, index, value):
        """ solves clues with a value between 1 and N
        removes posibilities which would obstruct view
        in cells closer to edge """
        # example: 3|1234|1234|1234|1234| N=4
        #   =>      |12  |123 |1234|1234|

        # @FIXME
        # code fragmentarisation
        value = int(value)
        nums = [i for i in range(1, self.size()+1)]
        if sides[side] == 'up':
            for row_index in range(value-1):
                numset = nums[-(value-1)+row_index:]
                self.contents[row_index][index] = self.contents[
                    row_index][index].difference(numset)
        if sides[side] == 'down':
            for row_index in range(value-1):
                numset = nums[-(value-1)+row_index:]
                self.contents[self.size()-row_index-1][index] = self.contents[
                    self.size()-row_index-1][index].difference(numset)
        if sides[side] == 'left':
            for column_index in range(value-1):
                numset = nums[-(value-1)+column_index:]
                self.contents[index][column_index] = self.contents[
                    index][column_index].difference(numset)
        if sides[side] == 'right':
            for column_index in range(value-1):
                numset = nums[-(value-1)+column_index:]
                self.contents[index][
                    self.size()-column_index-1] = self.contents[
                        index][self.size()-column_index-1].difference(numset)

    def sudoku_rule(self, value):
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
            else:
                raise CannotSolveError()

    def solve_initial_clues(self):
        for side, row in enumerate(self.clues):
            for index, value in enumerate(row):
                if value == str(self.size()):
                    self.fill_max(side, index)
                elif value == '1':
                    self.set_biggest(side, index)
                elif value in [str(val) for val in range(2, self.size())]:
                    self.fill(side, index, value)
                else:
                    raise(WrongDataError())
