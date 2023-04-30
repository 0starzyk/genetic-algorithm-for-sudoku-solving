import numpy as np
import random

class SudokuSolution:
    def __init__(self):
        self.filled_sudoku = np.copy(SudokuSolution.unsolved_sudoku)
        self.cost = self.calculate_cost()
        for square in self.filled_sudoku:
            SudokuSolution.random_fill_one_square(square)

    def crossover(self, other):
        child = SudokuSolution()
        child.filled_sudoku = np.array([random.choice(list(zip(self.filled_sudoku, other.filled_sudoku))[i]) for i in range(9)])
        child.mutate(0.2)
        return child

    def mutate(self, probability):
        for square_index in range(9):
            if probability > random.random():
                square = SudokuSolution.unsolved_sudoku[square_index]
                unfilled_box_indices = np.where(square == 0)[0]
                first_random_position, second_random_position = random.choice(unfilled_box_indices), random.choice(unfilled_box_indices)
                self.filled_sudoku[square_index, first_random_position], self.filled_sudoku[square_index, second_random_position] = self.filled_sudoku[square_index, second_random_position], self.filled_sudoku[square_index, first_random_position]

    def calculate_cost(self):
        filled_sudoku_array_row_form = self.get_row_form_sudoku_array(self.filled_sudoku)
        cost_value = 0
        for row in filled_sudoku_array_row_form:
            cost_value += len(np.unique(row))
        for row in filled_sudoku_array_row_form.T:
            cost_value += len(np.unique(row))
        return cost_value

    def print_filled_sudoku(self):
        filled_sudoku_array_row_form = SudokuSolution.get_row_form_sudoku_array(self.filled_sudoku)
        for row in filled_sudoku_array_row_form:
            print(" ".join(map(str, row)))

    @staticmethod
    def get_row_form_sudoku_array(square_form_sudoku_array):
        result_array = np.empty((0, 9), dtype=np.int64)
        for i in (0, 3, 6):
            for j in (0, 3, 6):
                row = np.concatenate((square_form_sudoku_array[i, j:j + 3], square_form_sudoku_array[i + 1, j:j + 3], square_form_sudoku_array[i + 2, j:j + 3]))
                result_array = np.append(result_array, [row], axis=0)
        return result_array

    @staticmethod
    def print_unsolved_sudoku():
        filled_sudoku_array_row_form = SudokuSolution.get_row_form_sudoku_array(SudokuSolution.unsolved_sudoku)
        for row in filled_sudoku_array_row_form:
            print(" ".join(map(str, row)))

    @staticmethod
    def init_unsolved_sudoku(sudoku_string: str):
        SudokuSolution.unsolved_sudoku = SudokuSolution.create_array_for_sudoku(sudoku_string)

    @staticmethod
    def create_array_for_one_square(string: str, position: int):
        return [int(string[position + (i % 3) + (i // 3) * 9]) for i in range(9)]

    @staticmethod
    def create_array_for_sudoku(string: str):
        return np.array([SudokuSolution.create_array_for_one_square(string, (i % 3) * 3 + (i // 3) * 27) for i in range(9)])

    @staticmethod
    def random_fill_one_square(square):
        missing_digits = [digit for digit in range(1, 10) if digit not in square]
        if len(missing_digits) == 0: return
        random.shuffle(missing_digits)
        j = 0
        for i in range(9):
            if square[i] == 0:
                square[i] = missing_digits[j]
                j += 1

    unsolved_sudoku = np.array([[0 for _ in range(9)] for _ in range(9)])