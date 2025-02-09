from search import NQueensProblem, depth_first_tree_search
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import từ Pillow để hiển thị ảnh quân hậu

"""
    # def depth_first_tree_search(problem):
    
    [Figure 3.7]
    Search the deepest nodes in the search tree first.
    Search through the successors of a problem to find a goal.
    The argument frontier should be an empty queue.
    Repeats infinitely in case of loops.
    

    frontier = [Node(problem.initial)]  # Stack

    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        frontier.extend(node.expand(problem))
    # return None

    frontier = [Node(problem.initial)]:
        frontier là danh sách dùng để lưu trữ các nút chờ được mở rộng (nó hoạt động như một stack).
        Node(problem.initial) là nút bắt đầu, được tạo từ trạng thái ban đầu của bài toán.

    while frontier::
        Vòng lặp while chạy cho đến khi frontier trống. Nếu còn nút để mở rộng, vòng lặp tiếp tục.

    node = frontier.pop():
        Lấy nút cuối cùng trong frontier để mở rộng. Tìm kiếm theo chiều sâu (depth-first) được thực hiện bằng cách lấy nút cuối cùng của danh sách (giống như hoạt động của stack).

    if problem.goal_test(node.state)::
        Kiểm tra xem trạng thái hiện tại (node.state) có phải là trạng thái đích không.
        Nếu trạng thái hiện tại là trạng thái đích, tức là bài toán đã được giải, hàm sẽ trả về node chứa lời giải.

    frontier.extend(node.expand(problem)):
        Nếu node chưa phải trạng thái đích, mở rộng nút đó bằng cách gọi node.expand(problem). Hàm này sẽ trả về danh sách các nút con từ node.
        Sau đó, các nút con này được thêm vào frontier để tiếp tục quá trình tìm kiếm.

    return None:
        Nếu không tìm thấy lời giải và frontier trống, hàm trả về None, biểu thị rằng không có lời giải cho bài toán.
"""

# Hàm giải bài toán N-Queens
def solve_partial_nqueens(n, initial_state):
    problem = NQueensProblem(n)
    problem.initial = initial_state
    solution = depth_first_tree_search(problem)
    if solution is None:
        return None
    return solution.state 

# Hàm vẽ bàn cờ và hiển thị quân hậu
def draw_chessboard(canvas, size, solution, queen_image):
    cell_size = 60
    canvas.delete("all")
    # Vẽ bàn cờ
    for row in range(size):
        for col in range(size):
            color = "#DEAA79" if (row + col) % 2 == 0 else "#FFE6A9"
            x1 = col * cell_size
            y1 = row * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill=color)  # Vẽ từng ô cờ
    # Đặt quân hậu trên bàn cờ
    for col, row in enumerate(solution):
        if row != -1:  # Nếu có quân hậu ở cột này
            x = col * cell_size
            y = row * cell_size
            canvas.create_image(x + cell_size // 2, y + cell_size // 2, image=queen_image)  # Hiển thị ảnh quân hậu

# Hàm xử lý đặt quân hậu đầu tiên
def place_queen(event, canvas, size, initial_state, queen_image):
    cell_size = 60  # Kích thước mỗi ô cờ
    col = event.x // cell_size  # Tính toán cột từ vị trí click của chuột
    row = event.y // cell_size  # Tính toán hàng từ vị trí click của chuột
    if initial_state[col] == -1:  # Chỉ cho phép đặt quân hậu ở cột trống
        initial_state[col] = row  # Cập nhật trạng thái ban đầu với vị trí quân hậu
        draw_chessboard(canvas, size, initial_state, queen_image)  # Vẽ lại bàn cờ với quân hậu mới

# Hàm reset bàn cờ
def reset_chessboard(canvas, size, initial_state, queen_image):
    initial_state[:] = [-1] * size  # Đặt lại trạng thái ban đầu là trống (không có quân hậu nào)
    draw_chessboard(canvas, size, initial_state, queen_image)  # Vẽ lại bàn cờ trống

# Giao diện Tkinter
def create_gui():
    size = 8  # Kích thước bàn cờ (8x8)
    cell_size = 60  # Kích thước mỗi ô của bàn cờ

    # Tạo cửa sổ chính
    root = tk.Tk()
    root.title("N-Queens Solver")  # Đặt tiêu đề cho cửa sổ

    # Canvas để vẽ bàn cờ
    canvas = tk.Canvas(root, width=size * cell_size, height=size * cell_size)
    canvas.pack()  # Đặt Canvas vào cửa sổ

    # Tải và thay đổi kích thước ảnh quân hậu
    queen_img = Image.open("queen.png")  # Tải ảnh quân hậu từ file
    queen_img = queen_img.resize((cell_size, cell_size))  
    queen_image = ImageTk.PhotoImage(queen_img)

    # Trạng thái ban đầu (bàn cờ trống)
    initial_state = [-1] * size  # -1 biểu thị rằng chưa có quân hậu nào được đặt

    # Vẽ bàn cờ trống với ảnh quân hậu
    draw_chessboard(canvas, size, initial_state, queen_image)  # Vẽ bàn cờ ban đầu

    # Gắn sự kiện click để đặt quân hậu
    canvas.bind("<Button-1>", lambda event: place_queen(event, canvas, size, initial_state, queen_image))

    # Frame chứa các nút "Solve" và "Reset"
    button_frame = tk.Frame(root)
    button_frame.pack()  # Đặt Frame chứa nút vào cửa sổ

    # Nút Solve
    def solve():
        solution = solve_partial_nqueens(size, tuple(initial_state))
        if solution is None:
            messagebox.showinfo("No Solution", "Không có lời giải cho bài toán N-Queens với trạng thái hiện tại.")
        else:
            draw_chessboard(canvas, size, solution, queen_image)
    solve_button = tk.Button(button_frame, text="Solve", command=solve)
    solve_button.grid(row=0, column=0, padx=5, pady=5)  # Đặt nút Solve vào Frame
    
    # Nút Reset
    reset_button = tk.Button(button_frame, text="Reset", command=lambda: reset_chessboard(canvas, size, initial_state, queen_image))
    reset_button.grid(row=0, column=1, padx=5, pady=5)  # Đặt nút Reset vào Frame

    # Hiển thị giao diện
    root.mainloop()  # Bắt đầu vòng lặp chính của Tkinter

# Chạy giao diện
create_gui()  # Gọi hàm tạo giao diện để bắt đầu chương trình
