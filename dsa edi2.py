import tkinter as tk
from tkinter import messagebox


# Sudoku boards for different levels
easy_board = [
    [2, 0, 5, 0, 0, 9, 0, 0, 4],
    [0, 0, 0, 0, 0, 0, 3, 0, 7],
    [7, 0, 0, 8, 5, 6, 0, 1, 0],
    [4, 5, 0, 7, 0, 0, 0, 0, 0],
    [0, 0, 9, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 8, 5],
    [0, 2, 0, 4, 1, 8, 0, 0, 6],
    [6, 0, 8, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 2, 0, 0, 7, 0, 8]
]

medium_board = [
    [0, 0, 6, 0, 9, 0, 2, 0, 0],
    [0, 0, 0, 7, 0, 2, 0, 0, 0],
    [0, 9, 0, 5, 0, 8, 0, 7, 0],
    [9, 0, 0, 0, 3, 0, 0, 0, 6],
    [7, 5, 0, 0, 0, 0, 0, 1, 9],
    [1, 0, 0, 0, 4, 0, 0, 0, 5],
    [0, 1, 0, 3, 0, 9, 0, 8, 0],
    [0, 0, 0, 2, 0, 1, 0, 0, 0],
    [0, 0, 9, 0, 8, 0, 1, 0, 0]
]

hard_board = [
    [0, 0, 0, 8, 0, 0, 0, 0, 0],
    [7, 8, 9, 0, 1, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 6, 1, 0, 0],
    [0, 0, 7, 0, 0, 0, 0, 5, 0],
    [5, 0, 8, 7, 0, 9, 3, 0, 4],
    [0, 4, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 3, 2, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 7, 0, 4, 3, 9],
    [0, 0, 0, 0, 0, 1, 0, 0, 0]
]

# Initialize the Tkinter application
root = tk.Tk()
root.title("LETS DO IT")
#backgroud color
root.config(bg="#dacef2")    # another color #6e6385

# Create the Sudoku grid
frame = tk.Frame(root, borderwidth=4, relief="solid")
frame.grid(row=0, column=0)

# Create the 3x3 grid border
subframe = tk.Frame(frame, borderwidth=2, relief="solid")
subframe.grid(row=0, column=0)

# Create the 9x9 grid
entries = []
for i in range(9):
    row_entries = []
    for j in range(9):
        entry = tk.Entry(frame, width=2, font=("Arial",20, "bold"), justify="center")
        entry.grid(row=i, column=j)
        row_entries.append(entry)
    entries.append(row_entries)

# Create the message label
message_label = tk.Label(root, text=" Do not repeat the same number in rows and columns",font=("Arial",15,"bold"), bg="lightblue")
message_label.grid(row=1, column=0, pady=10)

# Create the number selection buttons
number_buttons_frame = tk.Frame(root)
number_buttons_frame.grid(row=0, column=1, padx=10)
number_buttons_frame.config(bg="light blue")
                            

def select_number(number):
    for row in entries:
        for entry in row:
            if entry["state"] == "normal" and entry.get() == "":
                entry.insert(tk.END, number)
                return

number_buttons = []
for i in range(1, 10):
    number_button = tk.Button(number_buttons_frame, text=i, width=2, font=("Arial", 12, "bold"),command=lambda num=i: select_number(num))
    number_button.grid(row=(i-1)//3, column=(i-1)%3, padx=2, pady=2)
    number_buttons.append(number_button)

# Create the Check Solution button
def check_solution():
    user_board = [[int(entry.get()) if entry.get() else 0 for entry in row] for row in entries]
    if solve_sudoku(user_board):
        if user_board == board:
            messagebox.showinfo("Sudoku", "Congratulations! You solved the puzzle correctly.")
        else:
            messagebox.showinfo("Sudoku", "Sorry, your solution is incorrect.")
    else:
        messagebox.showinfo("Sudoku", "Sorry, your solution is incorrect.")

check_button = tk.Button(root, text="Check Solution", command=check_solution)
check_button.grid(row=2, column=0, pady=10)
check_button.config(bg="light blue")

# Create the Levels buttons
levels_frame = tk.Frame(root)
levels_frame.grid(row=0, column=2, padx=10)
levels_frame.config(bg="light blue")

def set_level(level):
    global board
    if level == "Easy":
        board = easy_board
    elif level == "Medium":
        board = medium_board
    elif level == "Hard":
        board = hard_board

    for i in range(9):
        for j in range(9):
            entry = entries[i][j]
            if board[i][j] != 0:
                entry.delete(0, tk.END)
                entry.insert(tk.END, str(board[i][j]))
                entry["state"] = "disabled"
            else:
                entry.delete(0, tk.END)
                entry["state"] = "normal"

levels = ["Easy", "Medium", "Hard"]
level_var = tk.StringVar()

for level in levels:
    level_button = tk.Button(levels_frame, text=level, width=10, font=("Arial", 12, "bold"),command=lambda lev=level: set_level(lev))
    level_button.pack(side=tk.TOP, pady=5)

# Sudoku solver functions
def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid(board, num, row, col):
            board[row][col] = num

            if solve_sudoku(board):
                return True

            board[row][col] = 0

    return False

def find_empty_cell(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

def is_valid(board, num, row, col):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

# Run the Tkinter event loop
root.mainloop()
