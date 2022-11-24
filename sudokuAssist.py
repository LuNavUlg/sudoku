from sudoku_utils import *


class Sudoku:
    def __init__(self, size=None, load=False, filename=""):
        self.size = size
        self.sudoku = []
        self.solution = []
        self.load = load
        self.filename = filename

    def sudoku_generate(self):
        if self.load:
            self.sudoku = sudoku_read(self.filename)
            self.size = len(self.sudoku)
        else:
            self.sudoku = sudoku_generate(self.size)

    def sudoku_print_quick(self):
        # Print the sudoku to the console and add row and column numbers
        if self.sudoku == []:
            print("impossible sudoku\n")
        N = len(self.sudoku)

        for line in self.sudoku:
            print("|", end="")
            for number in line:
                if N > 9 and number < 10:
                    print(" ", end="")
                print(" " if number == 0 else str(number), end="")
                print("|", end="")
            print("\n", end="")

    def sudoku_print_board(self):
        # Print the sudoku to the console and add row and column numbers
        if self.sudoku == []:
            print("impossible sudoku\n")
        N = len(self.sudoku)

        # Print the column numbers before the sudoku
        print("  ", end="")
        for i in range(N):
            print(" " + str(i + 1), end="")
        print("\n", end="")
        for (i, line) in enumerate(self.sudoku):

            # Print the row number
            print(str(i + 1) + " ", end="")
            print("|", end="")
            # Print the sudoku
            for number in line:
                if N > 9 and number < 10:
                    print(" ", end="")
                print(" " if number == 0 else str(number), end="")
                print("|", end="")
            print("\n", end="")

    def sudoku_solve(self):
        self.solution = sudoku_solve(self.sudoku)


print("Welcome to Sudoku Assist!")
while True:
    print("Do you want to load a sudoku from a file or generate a new one?")
    print("1. Load from file")
    print("2. Generate new sudoku")
    choice = input("Enter your choice: ")
    if choice == "1":
        filename = input("Enter the filename: ")
        sudoku = Sudoku(load=True, filename=filename)
    elif choice == "2":
        size = int(input("Enter the size of the sudoku: "))
        sudoku = Sudoku(size=size)
        print("Generating Sudoku of size {}...".format(size))
    sudoku.sudoku_generate()
    sudoku.sudoku_print_quick()

    print("Do you want to play with this Sudoku? (y/n)")
    answer = input()
    if answer == "y":
        print("Let's play!")
        break
    elif answer == "n":
        print("Let's try another one!")
    else:
        print("Please enter y or n.")

# Game loop
while True:
    print("What do you want to do?")
    sudoku.sudoku_print_board()
    print("1. Add a number")
    print("2. Remove a number")
    print("3. Abandon the game and solve the sudoku")
    print("4. Check if the sudoku is solved")
    print("5. Quit the game")

    choice = input("Enter your choice: ")
    if choice == "1":
        row = int(input("Enter the row number: "))
        col = int(input("Enter the column number: "))
        number = int(input("Enter the number: "))
        sudoku.sudoku[row - 1][col - 1] = number

    elif choice == "2":
        row = int(input("Enter the row number: "))
        col = int(input("Enter the column number: "))
        sudoku.sudoku[row - 1][col - 1] = 0

    elif choice == "3":
        print("Solving the sudoku...")
        print("Well done, maybe you can solve it yourself next time!")
        sudoku.sudoku_solve()
        sudoku.sudoku_print_board()
        break

    elif choice == "4":
        sudoku.sudoku_solve()
        if sudoku.sudoku == sudoku.solution:
            print("Congratulations! You solved the sudoku!")
        else:
            print("The sudoku is not solved yet.")

    elif choice == "5":
        print("Thank you for playing!")
        break
