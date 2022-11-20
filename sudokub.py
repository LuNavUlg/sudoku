#!/usr/bin/python

import sys
import subprocess
import random
from sudoku_utils import *

######################################################################
#                       UTILS                                       #
######################################################################


from enum import Enum


class Mode(Enum):
    SOLVE = 1
    UNIQUE = 2
    CREATE = 3
    CREATEMIN = 4
    TEST_SOLVE = 5


OPTIONS = {}
OPTIONS["-s"] = Mode.SOLVE
OPTIONS["-u"] = Mode.UNIQUE
OPTIONS["-c"] = Mode.CREATE
OPTIONS["-cm"] = Mode.CREATEMIN
OPTIONS["-ts"] = Mode.TEST_SOLVE

if len(sys.argv) != 3 and not sys.argv[1] in OPTIONS:
    sys.stdout.write("./sudokub.py <operation> <argument>\n")
    sys.stdout.write("     where <operation> can be -s, -u, -c, -cm\n")
    sys.stdout.write(
        "  ./sudokub.py -s <input>.txt: solves the Sudoku in input, whatever its size\n"
    )
    sys.stdout.write(
        "  ./sudokub.py -u <input>.txt: check the uniqueness of solution for Sudoku in input, whatever its size\n"
    )
    sys.stdout.write(
        "  ./sudokub.py -c <size>: creates a Sudoku of appropriate <size>\n"
    )
    sys.stdout.write(
        "  ./sudokub.py -cm <size>: creates a Sudoku of appropriate <size> using only <size>-1 numbers\n"
    )
    sys.stdout.write("    <size> is either 4, 9, 16, or 25\n")
    exit("Bad arguments\n")

mode = OPTIONS[sys.argv[1]]
if mode == Mode.SOLVE or mode == Mode.UNIQUE:
    filename = str(sys.argv[2])
    sudoku = sudoku_read(filename)
    N = len(sudoku)
    myfile = open("sudoku.cnf", "w")
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
    sys.stdout.write("sudoku\n")
    sudoku_print(sys.stdout, sudoku)
    sudoku = sudoku_solve("sudoku.cnf")
    sys.stdout.write("\nsolution\n")
    sudoku_print(sys.stdout, sudoku)
    if sudoku != [] and mode == Mode.UNIQUE:
        myfile = open("sudoku.cnf", "a")
        sudoku_other_solution_constraint(myfile, sudoku)
        myfile.close()
        sudoku = sudoku_solve("sudoku.cnf")
        if sudoku == []:
            sys.stdout.write("\nsolution is unique\n")
        else:
            sys.stdout.write("\nother solution\n")
            sudoku_print(sys.stdout, sudoku)
elif mode == Mode.CREATE:
    size = int(sys.argv[2])
    sudoku = sudoku_generate(size)
    sys.stdout.write("\ngenerated sudoku\n")
    sudoku_print(sys.stdout, sudoku)
elif mode == Mode.CREATEMIN:
    size = int(sys.argv[2])
    sudoku = sudoku_generate(size, True)
    sys.stdout.write("\ngenerated sudoku\n")
    sudoku_print(sys.stdout, sudoku)
elif mode == Mode.TEST_SOLVE:
    # Test the solver on all 9x9 Sudokus
    false = 0
    print("Testing the solver on all 9x9 Sudokus...")
    for i in range(100):
        number = str(i) if i >= 10 else "0" + str(i)
        filename = "sudoku9x9/sudoku" + number + ".txt"

        # Read the Sudoku
        sudoku = sudoku_read(filename)
        N = len(sudoku)
        myfile = open("sudoku.cnf", "w")
        # Notice that this may not be correct for N > 9
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

        # Get solution
        solution_path = "sudoku9x9-sol/sudoku" + number + ".txt"
        sudoku_true = sudoku_read(solution_path)

        # Check that the solution is correct
        if sudoku != sudoku_true:
            false += 1
            print("Error in sudoku " + str(i))

        if sudoku != [] and mode == Mode.UNIQUE:
            myfile = open("sudoku.cnf", "a")
            sudoku_other_solution_constraint(myfile, sudoku)
            myfile.close()
            sudoku = sudoku_solve("sudoku.cnf")
            if sudoku == []:
                sys.stdout.write("\nsolution is unique\n")
            else:
                sys.stdout.write("\nother solution\n")
                sudoku_print(sys.stdout, sudoku)

    if false == 0:
        print("OK\n")
    else:
        print("\nNumber of false solutions for 9x9 sudokus: " + str(false))

    # Test the solver on all 16x16 Sudokus
    false = 0
    print("Testing the solver on all 16x16 Sudokus...")
    for i in range(10):
        number = str(i) if i >= 10 else "0" + str(i)
        filename = "sudoku16x16/sudoku" + number + ".txt"

        # Read the Sudoku
        sudoku = sudoku_read(filename)
        N = len(sudoku)
        myfile = open("sudoku.cnf", "w")
        # Notice that this may not be correct for N > 9
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
        sudoku = sudoku_solve("sudoku.cnf")

        # Get solution
        solution_path = "sudoku16x16-sol/sudoku" + number + ".txt"
        sudoku_true = sudoku_read(solution_path)

        # Check that the solution is correct
        if sudoku != sudoku_true:
            false += 1
            print("Error in sudoku " + str(i))
            print("\nSolution found:\n")
            sudoku_print(sys.stdout, sudoku)
            print("\nTrue solution:\n")
            sudoku_print(sys.stdout, sudoku_true)

        if sudoku != [] and mode == Mode.UNIQUE:
            myfile = open("sudoku.cnf", "a")
            sudoku_other_solution_constraint(myfile, sudoku)
            myfile.close()
            sudoku = sudoku_solve("sudoku.cnf")
            if sudoku == []:
                sys.stdout.write("\nsolution is unique\n")
            else:
                sys.stdout.write("\nother solution\n")
                sudoku_print(sys.stdout, sudoku)

    if false == 0:
        print("OK\n")
    else:
        print("\nNumber of false solutions for 16x16 sudokus: " + str(false))

    # Test the solver on all 25x25 Sudokus
    false = 0
    print("Testing the solver on all 25x25 Sudokus...")

    for i in range(4):
        number = str(i) if i >= 10 else "0" + str(i)
        filename = "sudoku25x25/sudoku" + number + ".txt"

        # Read the Sudoku
        sudoku = sudoku_read(filename)
        N = len(sudoku)
        myfile = open("sudoku.cnf", "w")
        # Notice that this may not be correct for N > 9
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
        sudoku = sudoku_solve("sudoku.cnf")

        # Get solution
        solution_path = "sudoku25x25-sol/sudoku" + number + ".txt"
        sudoku_true = sudoku_read(solution_path)

        # Check that the solution is correct
        if sudoku != sudoku_true:
            false += 1
            print("Error in sudoku " + str(i))

        if sudoku != [] and mode == Mode.UNIQUE:
            myfile = open("sudoku.cnf", "a")
            sudoku_other_solution_constraint(myfile, sudoku)
            myfile.close()
            sudoku = sudoku_solve("sudoku.cnf")
            if sudoku == []:
                sys.stdout.write("\nsolution is unique\n")
            else:
                sys.stdout.write("\nother solution\n")
                sudoku_print(sys.stdout, sudoku)

    if false == 0:
        print("OK\n")
    else:
        print("\nNumber of false solutions for 25x25 sudokus: " + str(false))

# Test creating a sudoku
# print("Generate a 9x9 sudoku\n")
# sudoku = Sudoku(9)
# print("\nempty \n")
# sudoku.print_sudoku()
# sudoku = sudoku.generate()
# print("\nintialized \n")
# sudoku.print_sudoku()
# print("\ndone \n")
## Test visualizing sudoku
# print("Generate visualization window\n")
# sudoku_game = SudokuGame(sudoku)
# print("\ndone\n")
