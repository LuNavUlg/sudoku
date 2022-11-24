import sys
import subprocess
import random


def output(s, myfile):
    myfile.write(s)


# Notice that the following function only works for N = 4 or N = 9
# It should be generalized to N = 16 and N = 25
def newlit(i, j, k, N, myfile):
    if N == 4 or N == 9:
        # Introduces 4x4x4 or 9x9x9 boolean variables to denote each possible value in each cell
        output(str(i) + str(j) + str(k) + " ", myfile)
    elif N == 16 or N == 25:
        # Variable names cannot be 0
        # We can pass i, j, k as integers
        # but the problem is that we could obtain numbers like 1116, which we won't be able to convert to split into i, j, k back
        # So we add 10 to each number so that they are all >= 10 and we can split them back
        # Example: (i, j, k) = (1, 1, 1) -> (i, j, k) = (11, 11, 11)
        # Another example: (i, j, k) = (1, 2, 3) -> (i, j, k) = (11, 12, 13)
        # A previously problematic example: (i, j, k) = (1, 1, 16) -> (i, j, k) = (11, 11, 26)

        i = i + 10
        j = j + 10
        k = k + 10

        output(str(i) + str(j) + str(k) + " ", myfile)


# Notice that the following function only works for N = 4 or N = 9
# It should be generalized to N = 16 and N = 25
def newposlit(i, j, k, N, myfile):
    if N == 4 or N == 9:
        output(str(i) + str(j) + str(k) + " ", myfile)

    elif N == 16 or N == 25:
        i = i + 10
        j = j + 10
        k = k + 10

        output(str(i) + str(j) + str(k) + " ", myfile)


# Notice that the following function only works for N = 4 or N = 9
# It should be generalized to N = 16 and N = 25
def newneglit(i, j, k, N, myfile):
    if N == 4 or N == 9:
        output("-" + str(i) + str(j) + str(k) + " ", myfile)

    elif N == 16 or N == 25:
        i = i + 10
        j = j + 10
        k = k + 10

        output("-" + str(i) + str(j) + str(k) + " ", myfile)


def newcl(myfile):
    output("0\n", myfile)


def newcomment(s, myfile):
    #        output("c %s\n"%s, myfile)
    output("", myfile)


def save_sudoku(sudoku, name, size):
    if sudoku == []:
        print("It is not possible to solve the sudoku because it is empty.")
        return
    # Save sudoku to file and add vertical separators
    with open(name + ".txt", "w") as file:
        for row in range(size):
            for col in range(size):
                file.write("|")
                if sudoku[row][col] == 0:
                    file.write(" ")
                else:
                    file.write(str(sudoku[row][col]))
                if col == size - 1:
                    file.write("|")

            file.write("\n")


def has_unique_solution(sudoku, size):
    """This function checks if the sudoku has a unique solution

    Args:
        sudoku (List[List]): A sudoku grid
        size (int): The size of the sudoku
    Returns:
        (bool): True if the sudoku has a unique solution, False otherwise
    """

    # Write the cnf file
    N = len(sudoku)
    myfile = open("sudoku.cnf", "w")
    # Notice that this may not be correct for N > 9 # TODO
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
    sudoku = sudoku_solve("sudoku.cnf")

    # If the sudoku is not solvable, return False
    if not sudoku:
        return False

    # If the sudoku is solvable, try to solve it again
    myfile = open("sudoku.cnf", "a")
    sudoku_other_solution_constraint(myfile, sudoku)
    myfile.close()
    sudoku = sudoku_solve("sudoku.cnf")
    if sudoku == []:
        return True
    else:
        return False


def possible_numbers(sudoku, row, col, size):
    """This function finds the possible numbers for a cell

    Args:
        sudoku (List[List]): A sudoku grid
        row (int): The row of the cell
        col (int): The column of the cell
        size (int): The size of the sudoku
    Returns:
        possible (List[int]): A list of possible numbers for the cell
    """

    # Initially, all numbers are possible
    possible = [i for i in range(1, size + 1)]

    # Check the row
    for i in range(size):
        if sudoku[row][i] in possible:
            possible.remove(sudoku[row][i])

    # Check the column
    for i in range(size):
        if sudoku[i][col] in possible:
            possible.remove(sudoku[i][col])

    # Check the box
    box_size = int(size**0.5)
    box_row = row // box_size
    box_col = col // box_size
    for i in range(box_row * box_size, (box_row + 1) * box_size):
        for j in range(box_col * box_size, (box_col + 1) * box_size):
            if sudoku[i][j] in possible:
                possible.remove(sudoku[i][j])

    return possible


def fill_grid(sudoku, size):
    """This function fills the sudoku grid with numbers

    Args:
        sudoku (List[List]): A sudoku grid to be filled
        size (int): The size of the sudoku
        file (file): The file to write the cnf file to
    Returns:
        sudoku (List[List]): A filled sudoku grid.
    """
    print("Filling grid...")

    # Initially, all cells are empty
    free_cells = [(i, j) for i in range(size) for j in range(size)]

    # While there are empty cells
    while free_cells:

        # Choose a random cell
        row, col = random.choice(free_cells)

        # Find the possible numbers for the cell
        possible = possible_numbers(sudoku, row, col, size)

        # Choose a random number from the possible numbers
        if possible:
            number = random.choice(possible)
            # Fill the cell with the number
            sudoku[row][col] = number
            free_cells.remove((row, col))

            # Write the cnf file
            N = len(sudoku)
            myfile = open("sudoku.cnf", "w")
            # Notice that this may not be correct for N > 9 # TODO
            if N == 4 or N == 9:
                myfile.write(
                    "p cnf "
                    + str(N)
                    + str(N)
                    + str(N)
                    + " "
                    + str(sudoku_constraints_number(sudoku))
                    + "\n"
                )
            elif N == 16 or N == 25:
                myfile.write(
                    "p cnf "
                    + str(N + 10)
                    + str(N + 10)
                    + str(N + 10)
                    + " "
                    + str(sudoku_constraints_number(sudoku))
                    + "\n"
                )

            sudoku_generic_constraints(myfile, N)
            sudoku_specific_constraints(myfile, sudoku)
            myfile.close()
            solution = sudoku_solve("sudoku.cnf")

            # If the sudoku is not solvable, undo the previous step and try again
            # with another number and another cell
            if not solution:
                sudoku[row][col] = 0
                free_cells.append((row, col))
                continue

        else:
            continue

    return sudoku


def nb_clues(sudoku, size):
    """This function counts the number of clues in a sudoku grid

    Args:
        sudoku (List[List]): A sudoku grid
        size (int): The size of the sudoku
    Returns:
        (int): The number of clues in the sudoku grid
    """
    clues = 0
    for row in range(size):
        for col in range(size):
            if sudoku[row][col] != 0:
                clues += 1
    return clues


def remove_values(sudoku, size, clues_limit):
    """This function removes values from the sudoku grid

    Args:
        sudoku (List[List]): A sudoku grid to remove values from
        size (int): The size of the sudoku
        clues_limit (bool): Indicates if the sudoku must contain size-1 clues in the end (True) or if it can contain more (False)

    Returns:
        sudoku (List[List]): A sudoku grid with some values removed.
    """

    # 2. Remove some values from the sudoku one by one and check if the sudoku still has a unique solution
    #   a. If the sudoku has a unique solution, continue removing values
    #   b. If the sudoku does not have a unique solution, put back the value that was removed and continue removing other values

    max_nb_clues = size - 1 if clues_limit else size**2

    print("Removing values...")

    # Make a list of all cells positions and shuffle it
    cells = [(i, j) for i in range(size) for j in range(size)]
    cells = random.sample(cells, len(cells))

    if clues_limit:
        print("Clues limit: " + str(max_nb_clues))
        while nb_clues(sudoku, size) > max_nb_clues:
            print("Number of remaining clues: " + str(nb_clues(sudoku, size)))
            row, col = cells.pop()
            value = sudoku[row][col]
            sudoku[row][col] = 0
            if not has_unique_solution(sudoku, size):
                sudoku[row][col] = value
                cells.append((row, col))  # Put back the value that was removed
                cells = random.sample(
                    cells, len(cells)
                )  # shuffle the list of cells again to avoid removing the same values
    else:
        while cells:

            # Choose a random cell
            row, col = cells.pop()

            # Remember the value of the cell
            value = sudoku[row][col]

            # Remove the value from the cell
            sudoku[row][col] = 0

            # Check if the sudoku has a unique solution
            if not has_unique_solution(sudoku, size):
                # If it does not, put back the value
                sudoku[row][col] = value

    return sudoku


# reads a sudoku from file
# columns are separated by |, lines by newlines
# Example of a 4x4 sudoku:
# |1| | | |
# | | | |3|
# | | |2| |
# | |2| | |
# spaces and empty lines are ignored
def sudoku_read(filename):
    myfile = open(filename, "r")
    sudoku = []
    N = 0
    for line in myfile:
        line = line.replace(" ", "")
        if line == "":
            continue
        line = line.split("|")
        if line[0] != "":
            exit("illegal input: every line should start with |\n")
        line = line[1:]
        if line.pop() != "\n":
            exit("illegal input\n")
        if N == 0:
            N = len(line)
            if N != 4 and N != 9 and N != 16 and N != 25:
                exit("illegal input: only size 4, 9, 16 and 25 are supported\n")
        elif N != len(line):
            exit("illegal input: number of columns not invariant\n")
        line = [int(x) if x != "" and int(x) >= 0 and int(x) <= N else 0 for x in line]
        sudoku += [line]
    return sudoku


# print sudoku on stdout
def sudoku_print(myfile, sudoku):
    if sudoku == []:
        myfile.write("impossible sudoku\n")
    N = len(sudoku)
    for line in sudoku:
        myfile.write("|")
        for number in line:
            if N > 9 and number < 10:
                myfile.write(" ")
            myfile.write(" " if number == 0 else str(number))
            myfile.write("|")
        myfile.write("\n")


# get number of constraints for sudoku
def sudoku_constraints_number(sudoku):

    N = len(sudoku)

    count = 4 * N * N * (1 + N * (N - 1) / 2)
    for line in sudoku:
        for number in line:
            if number > 0:
                count += 1

    return count


# prints the generic constraints for sudoku of size N
def sudoku_generic_constraints(myfile, N):

    if N == 4:
        n = 2
    elif N == 9:
        n = 3
    elif N == 16:
        n = 4
    elif N == 25:
        n = 5
    else:
        exit("Only supports size 4, 9, 16 and 25")

    # Here should come the constraint generation
    # ...
    # We will characterize the following propositions : p(r, c, d) = "the number d is in the cell (r, c)"
    # p(r, c, d) is true if and only if the number d is in the cell (r, c), and false otherwise

    # We will use the following rules to generate the constraints :
    # 1. Each cell must contain exactly one number :
    #    for each row
    #         and for each column
    #            p(r,c,1) or p(r,c,2) or ... or p(r,c,N)
    for r in range(1, N + 1):
        for c in range(1, N + 1):
            for d in range(1, N + 1):
                newposlit(r, c, d, N, myfile)
            newcl(myfile)

    # 2. Each number must appear exactly once in each row :
    for c in range(1, N + 1):
        for d in range(1, N + 1):
            for r in range(1, N):
                for s in range(r + 1, N + 1):
                    newneglit(r, c, d, N, myfile)  # negative
                    newneglit(s, c, d, N, myfile)  # negative
                    newcl(myfile)

    # 3. Each number must appear exactly once in each column :
    for r in range(1, N + 1):
        for d in range(1, N + 1):
            for c in range(1, N):
                for s in range(c + 1, N + 1):
                    newneglit(r, c, d, N, myfile)  # negative
                    newneglit(r, s, d, N, myfile)  # negative
                    newcl(myfile)

    # 4. Each number must appear exactly once in each N*N block :
    for d in range(1, N + 1):
        for r in range(0, n):
            for c in range(0, n):
                for i in range(1, n + 1):
                    for j in range(1, n + 1):
                        for k in range(i + 1, n):
                            newneglit(r * n + i, c * n + j, d, N, myfile)
                            newneglit(r * n + k, c * n + j, d, N, myfile)  # negative
                            newcl(myfile)

    for d in range(1, N + 1):
        for r in range(0, n):
            for c in range(0, n):
                for i in range(1, n + 1):
                    for j in range(1, n + 1):
                        for k in range(j + 1, n + 1):
                            for l in range(1, n + 1):
                                newneglit(
                                    r * n + i, c * n + j, d, N, myfile
                                )  # negative
                                newneglit(
                                    r * n + l, c * n + k, d, N, myfile
                                )  # negative
                                newcl(myfile)


def sudoku_specific_constraints(myfile, sudoku):

    N = len(sudoku)

    # The sudoku must contain the values given in the input file initially, and no other values
    # I see in the outpout that there is a problem with the encoding of the sudoku
    # The initial values are not correctly placed in the sudoku (see the output file)
    # The following code should be fixed
    for r in range(1, N + 1):
        for c in range(1, N + 1):
            if sudoku[r - 1][c - 1] != 0:
                newposlit(r, c, sudoku[r - 1][c - 1], N, myfile)
                newcl(myfile)
            else:
                for d in range(1, N + 1):
                    newposlit(r, c, d, N, myfile)
                newcl(myfile)


def sudoku_other_solution_constraint(myfile, sudoku):

    N = len(sudoku)

    # Here should come the constraint generation
    # ...
    # To find a solution that is different from the one given in argument
    # we must encode the fact that the content of the sudoku is different from the one given in argument

    # At least one value is different
    # for each cell of the other solution, we must encode that at least one cell is different from the one given in argument
    # For instance, if the found solution is :
    # 1 2 3 4
    # 2 3 4 1
    # 3 4 1 2
    # 4 1 2 3
    # We must encode for the new solution that
    # either the cell (1,1) is different from 1 or the cell (1,2) is different from 2 or the cell (1,3) is different from 3 or the cell (1,4) is different from 4 or...
    # not p(1,1,1) or not p(1,2,2) or not p(1,3,3) or not p(1,4,4) or...
    for i in range(N):
        for j in range(N):
            value = sudoku[i][j]
            newneglit(i + 1, j + 1, value, N, myfile)
        newcl(myfile)


def sudoku_solve(filename):
    command = "java -jar org.sat4j.core.jar sudoku.cnf"
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    out, err = process.communicate()
    for line in out.split(b"\n"):
        line = line.decode("utf-8")
        if line == "" or line[0] == "c":
            continue
        if line[0] == "s":
            if line != "s SATISFIABLE":
                return []
            continue
        if line[0] == "v":
            line = line[2:]
            units = line.split()
            if units.pop() != "0":
                print("Error: last unit is not 0")
                exit("strange output from SAT solver:" + line + "\n")
            units = [int(x) for x in units if int(x) >= 0]
            N = len(units)
            if N == 16:
                N = 4
            elif N == 81:
                N = 9
            elif N == 256:
                N = 16
            elif N == 625:
                N = 25
            else:
                print("Error: number of units is not 16, 81, 256 or 625")
                exit("strange output from SAT solver:" + line + "\n")
            sudoku = [[0 for i in range(N)] for j in range(N)]
            # Notice that the following function only works for N = 4 or N = 9
            if N == 4 or N == 9:
                # This function does the following:
                # 1. For each unit in units, it extracts the i, j, k values
                # 2. It sets sudoku[i][j] = k
                for number in units:
                    sudoku[number // 100 - 1][(number // 10) % 10 - 1] = number % 10
            elif N == 16 or N == 25:
                # This function does the following:
                # 1. For each unit in units
                # 2. Get digits of the number two by two
                # 3. i=first and second digit, j=third and fourth digit, k=fifth and sixth digit
                # 4. Remove 10 from i, j, k
                # 5. Set sudoku[i-1][j-1] = k

                for number in units:
                    i = int(str(number)[:2]) - 10
                    j = int(str(number)[2:4]) - 10
                    k = int(str(number)[4:]) - 10
                    sudoku[i - 1][j - 1] = k

            return sudoku
        print("Error: line does not start with c, s or v")
        exit("strange output from SAT solver:" + line + "\n")
        return []


def sudoku_generate(size, nb_clues=False):
    # Generate a sudoku of size with a unique solution
    sudoku = [[0 for i in range(size)] for j in range(size)]
    unique = False

    while not unique:  # While the sudoku does not accept unique solution

        # 1. Generate a complete solution using backtracking that fills the sudoku
        sudoku = fill_grid(sudoku, size)
        sudoku_print(sys.stdout, sudoku)

        # 2. Remove some values from the sudoku one by one and check if the sudoku still has a unique solution
        #   a. If the sudoku has a unique solution, continue removing values
        #   b. If the sudoku does not have a unique solution, put back the value that was removed and continue removing other values
        sudoku = remove_values(sudoku, size, nb_clues)

        # Check if the sudoku has a unique solution
        if has_unique_solution(sudoku, size):
            unique = True

    save_sudoku(sudoku, "new_sudoku", size)

    return sudoku


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
