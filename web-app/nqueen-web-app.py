import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
from search import NQueensProblem, depth_first_tree_search

st.title("8 Queens Solver")
chessboard_path = "chessboard.bmp"
queen_image_path = "queen.png"

# Mở ảnh bàn cờ và quân hậu
bg_image = Image.open(chessboard_path).convert('RGB')
queen_img = Image.open(queen_image_path).convert('RGBA')

# Khởi tạo session state nếu chưa có
if 'canvas_image' not in st.session_state:
    st.session_state['canvas_image'] = bg_image.copy()
    st.session_state['initial_state'] = [-1] * 8  # Khởi tạo trạng thái ban đầu (chưa có quân hậu)
    st.session_state['points'] = []  # Lưu các điểm đã đặt quân hậu
    st.session_state['canvas_key'] = 0  # Khởi tạo khóa của canvas để cập nhật

# Tạo canvas cho phép người dùng đặt quân hậu
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=3,
    stroke_color="#000000",
    background_image=st.session_state['canvas_image'],
    height=bg_image.height,
    width=bg_image.width,
    drawing_mode="point",
    key=f"canvas_{st.session_state['canvas_key']}"
)

# Xử lý điểm người dùng nhấp chọn trên canvas
if canvas_result.json_data is not None:
    for obj in canvas_result.json_data["objects"]:
        # Tọa độ pixel của điểm
        px = obj['left']
        py = obj['top']

        # Chuyển tọa độ pixel sang tọa độ trên lưới
        col = int(px // (bg_image.width / 8))
        row = int(py // (bg_image.height / 8))

        # Kiểm tra nếu điểm hợp lệ và chưa có quân hậu
        if st.session_state['initial_state'][col] == -1:
            st.session_state['initial_state'][col] = row
            st.session_state['points'].append((col, row))  # Lưu điểm đã đặt quân hậu

            # Cập nhật canvas với quân hậu đầu tiên
            frame = st.session_state['canvas_image'].copy()
            cell_width = bg_image.width // 8
            cell_height = bg_image.height // 8
            queen_img_resized = queen_img.resize((cell_width, cell_height))

            # Vẽ quân hậu tại vị trí đã chọn
            x = col * cell_width
            y = row * cell_height
            frame.paste(queen_img_resized, (x, y), queen_img_resized)

            # Cập nhật lại ảnh nền với quân hậu đã vẽ
            st.session_state['canvas_image'] = frame

            # Hiển thị lại canvas với ảnh nền mới
            st.session_state['canvas_key'] += 1  # Tăng giá trị của canvas_key để làm mới canvas
            canvas_result = st_canvas(
                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=3,
                stroke_color="#000000",
                background_image=st.session_state['canvas_image'],
                height=bg_image.height,
                width=bg_image.width,
                drawing_mode="point",
                key=f"canvas_{st.session_state['canvas_key']}"
            )

# Hiển thị nút Solve để giải bài toán
if st.button("Solve"):
    problem = NQueensProblem(8)
    initial_state = tuple(st.session_state['initial_state'])
    problem.initial = initial_state

    # Sử dụng thuật toán tìm kiếm theo chiều sâu từ aima để giải bài toán
    solution = depth_first_tree_search(problem)

    if solution:
        solution_state = solution.state
        frame = bg_image.copy()

        # Đặt kích thước quân hậu để phù hợp với kích thước của ô cờ
        cell_width = bg_image.width // 8
        cell_height = bg_image.height // 8
        queen_img_resized = queen_img.resize((cell_width, cell_height))

        # Vẽ tất cả các quân hậu lên bàn cờ
        for col, row in enumerate(solution_state):
            if row != -1:
                x = col * cell_width
                y = row * cell_height
                frame.paste(queen_img_resized, (x, y), queen_img_resized)  # Dán hình quân hậu lên bàn cờ, sử dụng alpha channel để không bị che nền

        # Cập nhật lại ảnh nền với lời giải
        st.image(frame, caption="Solution with 8 Queens")

# Nút Reset để làm lại từ đầu, khởi tạo lại bài toán
if st.button("Reset"):
    # Đặt lại trạng thái ban đầu: cả quân hậu và canvas đều trở lại như mới
    st.session_state['initial_state'] = [-1] * 8
    st.session_state['canvas_image'] = bg_image.copy()
    st.session_state['points'] = []  # Đặt lại các điểm đã chọn
    st.session_state['canvas_key'] += 1  # Tăng giá trị của canvas_key để làm mới canvas

    # Tạo lại canvas với bàn cờ trống
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=3,
        stroke_color="#000000",
        background_image=st.session_state['canvas_image'],
        height=bg_image.height,
        width=bg_image.width,
        drawing_mode="point",
        key=f"canvas_{st.session_state['canvas_key']}"
    )
