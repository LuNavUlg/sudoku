import random

import soupsieve
import pygame
import numpy as np
from sudokub import sudoku_generic_constraints, sudoku_specific_constraints


class Cell:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col

    def __str__(self):
        return str(self.value)

    def get_coords(self):
        return (self.row, self.col)

    def draw_cell(cell_size):
        for i in range(2):
            pygame.draw.line(
                screen,
                BLACK,
                (x, y + i * cell_size),
                (x + cell_size, y + i * cell_size),
            )
            pygame.draw.line(
                screen,
                BLACK,
                (x + i * cell_size, y),
                (x + i * cell_size, y + cell_size),
            )


class Sudoku:
    def __init__(self, size):
        self.size = size
        self.board = [[0 for x in range(size)] for y in range(size)]

    def __str__(self):
        return str(self.board)

    def fill_grid(self):
        # Go through each square, and check each number in each square to see if we
        # can generate a valid solution with it
        for row in range(self.size):
            for col in range(self.size):
                # If the square is empty, we need to fill it
                if self.board[row][col] == 0:
                    # Choose a random number between 1 and N for this square
                    # We need to check if this number is valid
                    # If it is, we can assign it to the square and move on
                    # If it is not, we need to try a different number
                    numbers = [i for i in range(1, self.size + 1)]
                    # Shuffle the numbers to generate different sudokus
                    numbers = random.sample(numbers, len(numbers))
                    for number in numbers:
                        # Encode in SAT format in cnf file
                        myfile.write(
                            "p cnf "
                            + str(N)
                            + str(N)
                            + str(N)
                            + " "
                            + str(sudoku_constraints_number(sudoku))
                            + "\n"
                        )
                        sudoku_generic_constraints(myfile, N)
                        sudoku_specific_constraints(myfile, sudoku)
                        myfile.close()

        return False

    def remove_cells(self):
        # Remove cells one by one, and check if the grid is still solvable
        # If the grid is still solvable, remove the cell, otherwise put it back

        # Remove a random (non-empty) cell from the grid
        row, col = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
        if self.board[row][col] == 0:
            return False

        self.board[row][col] = 0

        # Solve the new grid with backtracking, check if the solution is unique
        solutions = self.solve()
        if len(solutions) != 1:
            self.board[row][col] = solutions[0][row][col]
            return False

    # Generate a sudoku that a unique solution
    def generate(self):

        # Backtracking algorithm to solve the sudoku
        # Incrementally builds a solution, and backtracks when it gets stuck

        # 1. Generate a complete solution using backtracking that fills the grid
        self.fill_grid()

        # 2. Remove cells one by one, and check if the grid is still solvable
        # 3. If the grid is still solvable, remove the cell, otherwise put it back
        self.remove_cells()

        return self

    def save(self, path):
        with open(path, "w") as f:
            for i in range(self.size):
                for j in range(self.size):
                    f.write(str(self.board[i][j]))
                f.write("")

    def load(self, path):
        with open(path, "r") as f:
            for i in range(self.size):
                line = f.readline()
                for j in range(self.size):
                    self.board[i][j] = int(line[j])

    def print_sudoku(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.board[i][j], end="")
            print("")
