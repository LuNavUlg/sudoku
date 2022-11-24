import tkinter as tk
import sys
from tkinter import ttk
from sudoku_utils import *


def saveSudoku(sudoku, N):
    save_sudoku(sudoku, "new_sudoku", N)


def createSudoku(canvas, create_window):
    global CREATED_SUDOKU
    CREATED_SUDOKU = []

    # Clear the grid to make sure it is empty (remove numbers and lines)
    canvas.delete("all")

    # Get the size of the sudoku
    N = 9

    size = 500

    # Create the sudoku grid
    for i in range(N):
        # Draw thicker lines every [sqrt(N)] lines
        if i % (N**0.5) == 0:
            canvas.create_line(0, size / N * i, size, size / N * i, width=3)
            canvas.create_line(size / N * i, 0, size / N * i, size, width=3)
        # Create the horizontal lines
        canvas.create_line(0, i * size / N, size, i * size / N, width=1)
        # Create the vertical lines
        canvas.create_line(i * size / N, 0, i * size / N, size, width=1)

    # Generate a sudoku
    sudoku = sudoku_generate(N)
    CREATED_SUDOKU = sudoku

    # Display the numbers in the sudoku grid
    for line in sudoku:
        for number in line:
            if number != 0:
                if N == 9 or N == 4:
                    font = ("Arial", 20)
                elif N == 16:
                    font = ("Arial", 15)
                elif N == 25:
                    font = ("Arial", 10)
                canvas.create_text(
                    size / N * (line.index(number) + 0.5),
                    size / N * (sudoku.index(line) + 0.5),
                    text=number,
                    font=font,
                )


def solveSudoku(sudoku, canvas, size):
    global SUDOKU_TO_SOLVE
    SUDOKU_TO_SOLVE = sudoku

    N = len(sudoku)
    # Solve the sudoku
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

    print(solution)

    # Print the solution in the sudoku grid (if it exists)
    if solution is not None:
        for line in solution:
            for number in line:
                if number != 0:
                    # Display numbers that were not in the original sudoku in green
                    if sudoku[solution.index(line)][line.index(number)] == 0:
                        if N == 9 or N == 4:
                            font = ("Arial", 20)
                        elif N == 16:
                            font = ("Arial", 15)
                        elif N == 25:
                            font = ("Arial", 10)
                        canvas.create_text(
                            size / N * (line.index(number) + 0.5),
                            size / N * (solution.index(line) + 0.5),
                            text=number,
                            font=font,
                            fill="green",
                        )


def solveSudokuDisp(file_name, solve_window, canvas):
    global SUDOKU_TO_SOLVE
    SUDOKU_TO_SOLVE = sudoku_read(file_name)
    sudoku = SUDOKU_TO_SOLVE

    # Get the size of the sudoku
    N = len(sudoku)

    # Clear the canvas to make sure it is empty (remove numbers and lines)
    canvas.delete("all")

    size = 500

    # Create the sudoku grid
    for i in range(N):
        # Draw thicker lines every [sqrt(N)] lines
        if i % (N**0.5) == 0:
            print("i = ", i)
            canvas.create_line(0, size / N * i, size, size / N * i, width=3)
            canvas.create_line(size / N * i, 0, size / N * i, size, width=3)
        # Create the horizontal lines
        canvas.create_line(0, i * size / N, size, i * size / N, width=1)
        # Create the vertical lines
        canvas.create_line(i * size / N, 0, i * size / N, size, width=1)

    # Display the numbers in the sudoku grid
    for line in sudoku:
        for number in line:
            if number != 0:
                if N == 9 or N == 4:
                    font = ("Arial", 20)
                elif N == 16:
                    font = ("Arial", 15)
                elif N == 25:
                    font = ("Arial", 10)
                canvas.create_text(
                    size / N * (line.index(number) + 0.5),
                    size / N * (sudoku.index(line) + 0.5),
                    text=number,
                    font=font,
                )


def seeSudokuDisp(file_name, see_window, canvas):
    global SUDOKU_TO_SEE
    SUDOKU_TO_SEE = sudoku_read(file_name)
    sudoku = SUDOKU_TO_SEE
    # Get the size of the sudoku
    N = len(sudoku)

    # Clear the canvas to make sure it is empty (remove numbers and lines)
    canvas.delete("all")

    size = 500

    # Create the sudoku grid
    for i in range(N):
        # Draw thicker lines every [sqrt(N)] lines
        if i % (N**0.5) == 0:
            canvas.create_line(0, size / N * i, size, size / N * i, width=3)
            canvas.create_line(size / N * i, 0, size / N * i, size, width=3)
        # Create the horizontal lines
        canvas.create_line(0, i * size / N, size, i * size / N, width=1)
        # Create the vertical lines
        canvas.create_line(i * size / N, 0, i * size / N, size, width=1)

    # Display the numbers in the sudoku grid
    for line in sudoku:
        for number in line:
            if number != 0:
                if N == 9 or N == 4:
                    font = ("Arial", 20)
                elif N == 16:
                    font = ("Arial", 15)
                elif N == 25:
                    font = ("Arial", 10)
                canvas.create_text(
                    size / N * (line.index(number) + 0.5),
                    size / N * (sudoku.index(line) + 0.5),
                    text=number,
                    font=font,
                )


def clickButton(action):
    if action == "solve":
        print("Solving...")
        global SUDOKU_TO_SOLVE
        SUDOKU_TO_SOLVE = []

        # Create a new window to display the sudoku
        solve_window = tk.Toplevel()
        solve_window.title("Sudoku solver")
        solve_window.iconbitmap("icon.ico")
        solve_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        ttk.Label(
            solve_window, text="Solve a sudoku", padding=20, font=("Arial", 20)
        ).pack()

        file_name = tk.StringVar()

        ttk.Label(
            solve_window,
            text="Please enter the file name of the sudoku you would like to solve...",
        ).pack()
        textbox = ttk.Entry(solve_window, width=30, textvariable=file_name).pack()

        solve_button = ttk.Button(
            solve_window,
            text="Choose",
            command=lambda: solveSudokuDisp(file_name.get(), solve_window, canvas),
        ).pack()

        # Display the sudoku in the window
        # Create a big white frame to contain the sudoku
        frame = tk.Frame(
            solve_window,
            bg="white",
            width=window_width,
            height=500,
            relief="solid",
            padx=10,
            pady=10,
        )
        frame.pack()

        canvas = tk.Canvas(frame, width=500, height=500, borderwidth=3, relief="solid")
        canvas.pack()

        # Create a button to go back to the main menu
        back_button = ttk.Button(
            solve_window,
            text="Back",
            command=lambda: solve_window.destroy(),
        ).pack()

        # Display a new button to go to solve this sudoku
        solve_button = ttk.Button(
            solve_window,
            text="See solution",
            command=lambda: solveSudoku(SUDOKU_TO_SOLVE, canvas, 500),
        ).pack()

        solve_window.mainloop()
        print(file_name.get())

    elif action == "see":
        print("Seeing...")
        global SUDOKU_TO_SEE
        SUDOKU_TO_SEE = []

        # Create a new window
        see_window = tk.Toplevel()
        see_window.title("See Sudoku")
        see_window.iconbitmap("icon.ico")

        # Center the window on the screen
        see_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        ttk.Label(
            see_window, text="See a sudoku", padding=20, font=("Arial", 20)
        ).pack()

        file_name = tk.StringVar()

        ttk.Label(
            see_window,
            text="Please enter the file name of the sudoku you would like to see...",
        ).pack()
        textbox = ttk.Entry(see_window, width=30, textvariable=file_name).pack()
        see_button = ttk.Button(
            see_window,
            text="Choose",
            command=lambda: seeSudokuDisp(file_name.get(), see_window, canvas),
        ).pack()

        # Display the sudoku in the window
        # Create a big white frame to contain the sudoku
        frame = tk.Frame(
            see_window,
            bg="white",
            width=window_width,
            height=500,
            relief="solid",
            padx=10,
            pady=10,
        )
        frame.pack()

        canvas = tk.Canvas(frame, width=500, height=500, borderwidth=3, relief="solid")
        canvas.pack()

        # Create a button to go back to the main menu
        back_button = ttk.Button(
            see_window,
            text="Back",
            command=lambda: see_window.destroy(),
        ).pack()

        # Display a new button to go to solve this sudoku
        solve_button = ttk.Button(
            see_window,
            text="Solve this sudoku",
            command=lambda: solveSudoku(SUDOKU_TO_SEE, canvas, 500),
        ).pack()

        see_window.mainloop()
        print(file_name.get())

    elif action == "create":
        global CREATED_SUDOKU
        CREATED_SUDOKU = []

        # Create a new window
        create_window = tk.Toplevel()
        create_window.title("Create Sudoku")
        create_window.iconbitmap("icon.ico")

        # Center the window on the screen
        create_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        ttk.Label(
            create_window, text="Create a sudoku", padding=20, font=("Arial", 20)
        ).pack()

        # Create a button to create the sudoku
        create_button = ttk.Button(
            create_window,
            text="Generate",
            command=lambda: createSudoku(canvas, create_window),
        ).pack()

        # Create a button to go back to the main menu
        back_button = ttk.Button(
            create_window,
            text="Back",
            command=lambda: create_window.destroy(),
        ).pack()

        # Create a frame to contain the sudoku
        frame = tk.Frame(
            create_window,
            bg="white",
            width=window_width,
            height=500,
            relief="solid",
            padx=10,
            pady=10,
        )
        frame.pack()

        # Create a canvas to display the sudoku
        canvas = tk.Canvas(frame, width=500, height=500, borderwidth=3, relief="solid")
        canvas.pack()

        solve_button = tk.Button(
            create_window,
            text="Solve this sudoku",
            command=lambda: solveSudoku(CREATED_SUDOKU, canvas, 500),
        ).pack()

        save_button = tk.Button(
            create_window,
            text="Save this sudoku",
            command=lambda: saveSudoku(CREATED_SUDOKU, 9),
        ).pack()

    elif action == "instructions":
        print("Showing instructions...")
        ttk.Label(window, text="Instructions", padding=20, font=("Arial", 20)).pack()
        ttk.Label(
            window,
            text="Welcome in this sudoku visualizer. Here are the few actions you are allowed to peform.",
        ).pack()
        ttk.Label(window, text="Have fun :)", padding=20).pack()
        ttk.Label(
            window,
            wraplength=window_width - 100,
            padding=10,
            text='1. Solve a sudoku. To do so you must enter the file name of the sudoku you\'d like to solve. Then, click the "Choose" button. The grid will be displayed in the window. To see the solution of the chosen sudoku click "See solution". A solution will be displayed in the window.',
        ).pack()
        ttk.Label(
            window,
            wraplength=window_width - 100,
            padding=10,
            text='2. Create a sudoku. An empty grid will appear. Click "Generate" to generate a new (9x9) sudoku. Please note that this process can take some time. Be patient. The grid will be displayed in the window. You can then solve the generated sudoku by clicking "Solve this sudoku". A solution will be displayed in the window. You can also save the generated sudoku by clicking "Save this sudoku". The generated sudoku will be saved in the root folder and have the name new_sudoku.txt.',
        ).pack()
        ttk.Label(
            window,
            wraplength=window_width - 100,
            padding=10,
            text='3. See a sudoku. To do so you must enter the file name of the sudoku you\'d like to see. Then, click the "Choose" button. The sudoku will be displayed in the window. You can then solve the chosen sudoku by clicking "Solve this sudoku". A solution will be displayed in the window.',
        ).pack()
        ttk.Label(
            window,
            wraplength=window_width - 100,
            padding=10,
            text="4. See instructions. Well, you are already here. So, you know what to do.",
        ).pack()
        ttk.Label(
            window,
            wraplength=window_width - 100,
            padding=10,
            text='5. Exit. To exit the program click "Exit".',
        ).pack()  # TODO


window = tk.Tk()
window.title("Sudoku solver")
window.iconbitmap("icon.ico")

# Center the window on the screen
window_width = 800
window_height = 800

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)

window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")


# Welcome message
welcome = ttk.Label(
    window, text="Welcome to Sudoku !", font=("Arial", 25), padding=10
).pack()
image = ttk.Label(
    window, image=tk.PhotoImage(file="./assets/sudoku.png"), padding=10
).pack()
question = ttk.Label(window, text="What would you like to do ?").pack()
solve_button = ttk.Button(
    window, text="Solve a Sudoku", command=lambda: clickButton("solve")
).pack()
create_button = ttk.Button(
    window, text="Create a Sudoku", command=lambda: clickButton("create")
).pack()
see_sudoku_button = ttk.Button(
    window, text="See a Sudoku", command=lambda: clickButton("see")
).pack()
instructions_button = ttk.Button(
    window, text="Instructions", command=lambda: clickButton("instructions")
).pack()

window.mainloop()
