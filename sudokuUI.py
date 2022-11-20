import tkinter as tk
import sys
from tkinter import ttk
from sudoku_utils import *


def solveSudoku(sudoku, N, canvas, size):
    # Solve the sudoku
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

    print(sudoku)

    # Print the solution in the sudoku grid (if it exists)
    if sudoku is not None:
        for line in sudoku:
            for number in line:
                if number != 0:
                    canvas.create_text(
                        size / N * (line.index(number) + 0.5),
                        size / N * (sudoku.index(line) + 0.5),
                        text=number,
                        font=("Arial", 20),
                        fill="green",
                    )


def solveSudokuDisp(file_name, solve_window):
    sudoku = sudoku_read(file_name)
    # Get the size of the sudoku
    N = len(sudoku)

    # If a sudoku was already displayed (3rd widget), delete it
    if len(solve_window.winfo_children()) == 4:
        solve_window.winfo_children()[3].destroy()

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

    size = 500

    # Create the sudoku grid
    for i in range(N):
        # Draw thicker lines every [sqrt(N)] lines
        if i % (N**0.5) == 0:
            canvas.create_line(
                0, size / N * i, size, size / N * i, fill="black", width=3
            )
            canvas.create_line(
                size / N * i, 0, size / N * i, size, fill="black", width=3
            )
        # Create the horizontal lines
        canvas.create_line(0, i * size / N, size, i * size / N, width=1)
        # Create the vertical lines
        canvas.create_line(i * size / N, 0, i * size / N, size, width=1)

    # Display the numbers in the sudoku grid
    for line in sudoku:
        for number in line:
            if number != 0:
                canvas.create_text(
                    size / N * (line.index(number) + 0.5),
                    size / N * (sudoku.index(line) + 0.5),
                    text=number,
                    font=("Arial", 20),
                )

    # Display a new button to go to solve this sudoku
    solve_button = ttk.Button(
        solve_window,
        text="Solve this sudoku",
        command=lambda: solveSudoku(sudoku, N, canvas, size),
    ).pack()


def seeSudokuDisp(file_name, see_window):
    sudoku = sudoku_read(file_name)
    # Get the size of the sudoku
    N = len(sudoku)

    # If a sudoku was already displayed (3rd widget), delete it
    if len(see_window.winfo_children()) == 4:
        see_window.winfo_children()[3].destroy()

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

    size = 500

    # Create the sudoku grid
    for i in range(N):
        # Draw thicker lines every [sqrt(N)] lines
        if i % (N**0.5) == 0:
            canvas.create_line(
                0, size / N * i, size, size / N * i, fill="black", width=3
            )
            canvas.create_line(
                size / N * i, 0, size / N * i, size, fill="black", width=3
            )
        # Create the horizontal lines
        canvas.create_line(0, i * size / N, size, i * size / N, width=1)
        # Create the vertical lines
        canvas.create_line(i * size / N, 0, i * size / N, size, width=1)

    # Display the numbers in the sudoku grid
    for line in sudoku:
        for number in line:
            if number != 0:
                canvas.create_text(
                    size / N * (line.index(number) + 0.5),
                    size / N * (sudoku.index(line) + 0.5),
                    text=number,
                    font=("Arial", 20),
                )

    # Display a new button to go to solve this sudoku
    solve_button = ttk.Button(
        see_window,
        text="Solve this sudoku",
        command=lambda: solveSudokuDisp(file_name, see_window),
    ).pack()


def clickButton(action):
    if action == "solve":
        print("Solving...")

        # Create a new window to display the sudoku
        solve_window = tk.Toplevel()
        solve_window.title("Sudoku solver")
        solve_window.iconbitmap("icon.ico")
        solve_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        file_name = tk.StringVar()

        ttk.Label(
            solve_window,
            text="Please enter the file name of the sudoku you would like to solve...",
        ).pack()
        textbox = ttk.Entry(solve_window, width=30, textvariable=file_name).pack()
        solve_button = ttk.Button(
            solve_window,
            text="Solve",
            command=lambda: solveSudokuDisp(file_name.get(), solve_window),
        ).pack()
        solve_window.mainloop()
        print(file_name.get())

    elif action == "see":
        # Create a new window
        see_window = tk.Toplevel()
        see_window.title("See Sudoku")
        see_window.iconbitmap("icon.ico")

        # Center the window on the screen
        see_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        file_name = tk.StringVar()

        ttk.Label(
            see_window,
            text="Please enter the file name of the sudoku you would like to see...",
        ).pack()
        textbox = ttk.Entry(see_window, width=30, textvariable=file_name).pack()
        see_button = ttk.Button(
            see_window,
            text="See",
            command=lambda: seeSudokuDisp(file_name.get(), see_window),
        ).pack()
        see_window.mainloop()
        print(file_name.get())

    elif action == "create":
        print("Creating...")
    elif action == "instructions":
        print("Showing instructions...")
        ttk.Label(window, text="Instructions").pack()
        ttk.Label(
            window,
            text="Welcome in this sudoku visualizer. Here are the few actions you are allowed to peform.\nHave fun :)",
        ).pack()
        ttk.Label(
            window,
            text="1. Solve a sudoku. To do so you must enter the file name of the sudoku you'd like to solve. Then, click the Solve button. A solution will be displayed in the window.\n 2. See a sudoku. To do so you must enter the file name of the sudoku you'd like to see. Then, click the See button. The sudoku will be displayed in the window.\n3. Create a sudoku. To do so you must enter the file name of the sudoku you'd like to create. Then, click the Create button. A new window will open. A new sudoku will be generated, and you will be able to save it.\n",
        ).pack()


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
welcome = ttk.Label(window, text="Welcome to Sudoku !").pack()
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
