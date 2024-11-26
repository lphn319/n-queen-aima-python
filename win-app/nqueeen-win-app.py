from search import NQueensProblem, Problem, depth_first_tree_search
import tkinter as tk
from PIL import Image, ImageTk  # Import từ Pillow

# Hàm giải bài toán N-Queens
def solve_partial_nqueens(n, initial_state):
    problem = NQueensProblem(n)
    problem.initial = initial_state  # Cập nhật trạng thái ban đầu
    solution = depth_first_tree_search(problem)
    return solution.state

# Hàm vẽ bàn cờ và hiển thị quân hậu
def draw_chessboard(canvas, size, solution, queen_image):
    cell_size = 60
    canvas.delete("all")  # Xóa bàn cờ cũ
    # Vẽ bàn cờ
    for row in range(size):
        for col in range(size):
            color = "#DEAA79" if (row + col) % 2 == 0 else "#FFE6A9"
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)
    # Đặt quân hậu
    for col, row in enumerate(solution):
        if row != -1:
            x = col * cell_size
            y = row * cell_size
            canvas.create_image(x + cell_size // 2, y + cell_size // 2, image=queen_image)

# Hàm xử lý đặt quân hậu đầu tiên
def place_queen(event, canvas, size, initial_state, queen_image):
    cell_size = 60
    col = event.x // cell_size
    row = event.y // cell_size
    if initial_state[col] == -1:  # Chỉ cho phép đặt quân hậu ở cột trống
        initial_state[col] = row
        draw_chessboard(canvas, size, initial_state, queen_image)

# Hàm reset bàn cờ
def reset_chessboard(canvas, size, initial_state, queen_image):
    initial_state[:] = [-1] * size  # Đặt lại trạng thái ban đầu là trống
    draw_chessboard(canvas, size, initial_state, queen_image)

# Giao diện Tkinter
def create_gui():
    size = 8  # Kích thước bàn cờ
    cell_size = 60

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("N-Queens Solver")

    # Canvas để vẽ bàn cờ
    canvas = tk.Canvas(root, width=size * cell_size, height=size * cell_size)
    canvas.pack()

    # Tải và thay đổi kích thước ảnh quân hậu
    queen_img = Image.open("queen.png")
    queen_img = queen_img.resize((cell_size, cell_size)) 
    queen_image = ImageTk.PhotoImage(queen_img)

    # Trạng thái ban đầu (bàn cờ trống)
    initial_state = [-1] * size

    # Vẽ bàn cờ trống với ảnh quân hậu
    draw_chessboard(canvas, size, initial_state, queen_image)

    # Gắn sự kiện click để đặt quân hậu
    canvas.bind("<Button-1>", lambda event: place_queen(event, canvas, size, initial_state, queen_image))

    # Frame chứa các nút "Solve" và "Reset"
    button_frame = tk.Frame(root)
    button_frame.pack()

    # Nút Solve
    solve_button = tk.Button(button_frame, text="Solve", command=lambda: draw_chessboard(canvas, size, solve_partial_nqueens(size, tuple(initial_state)), queen_image))
    solve_button.grid(row=0, column=0, padx=5, pady=5)
    
    # Nút Reset
    reset_button = tk.Button(button_frame, text="Reset", command=lambda: reset_chessboard(canvas, size, initial_state, queen_image))
    reset_button.grid(row=0, column=1, padx=5, pady=5)

    # Hiển thị giao diện
    root.mainloop()

# Chạy giao diện
create_gui()
