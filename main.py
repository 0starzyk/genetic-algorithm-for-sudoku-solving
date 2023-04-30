import numpy as np
import random
import SudokuSolution


def print_sudoku_string(sudoku_string: str):
    for i in range(len(sudoku_string)):
        if i % 9 == 0:
            print(" ".join(sudoku_string[i:i+9]))


if __name__ == '__main__':
    sudoku_string = "000260701680070090190004500820100040004602900050003028009300074040050036703018000"
    print_sudoku_string(sudoku_string)

    SudokuSolution.init_unsolved_sudoku(sudoku_string)
    population = [SudokuSolution() for _ in range(50)]

    population.sort(key=lambda member: member.calculate_cost(), reverse=True)
    print([member.calculate_cost() for member in population])

    for i in range(1000):
        if population[0].calculate_cost() == 162:
            print(i)
            break

        population = population[0:25]

        for member in population[0:25]:
            population.append(member.crossover(random.choice(population)))

        population.sort(key=lambda member: member.calculate_cost(), reverse=True)
        print([member.calculate_cost() for member in population])

    population[0].print_filled_sudoku()
