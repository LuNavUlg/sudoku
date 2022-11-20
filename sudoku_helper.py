import random
from sudoku_utils import possible_numbers


def generate_non_unique_sudoku():
    """Any valid 9x9 grid with 16 or fewer numbers on it will have multiple solutions."""

    # Generate empty grid of size 9x9
    sudoku = [[0 for _ in range(9)] for _ in range(9)]

    # Randomly fill 16 cells with numbers
    for _ in range(16):
        row = random.randint(0, 8)
        col = random.randint(0, 8)

        # Find possible numbers for cell
        possible = possible_numbers(sudoku, row, col, 9)

        # Fill cell with random number from possible numbers
        sudoku[row][col] = random.choice(possible)

    # Save sudoku to file and add vertical separators
    with open("non_unique_sudoku.txt", "w") as file:
        for row in range(9):
            for col in range(9):
                file.write("|")
                if sudoku[row][col] == 0:
                    file.write(" ")
                file.write(str(sudoku[row][col]))

            file.write("\n")

    return sudoku
