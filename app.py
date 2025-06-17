import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import numpy as np

# --- Knight's Tour Algorithm (Warnsdorff's rule) ---
# This is the Python version of the algorithm.
DIR = [
    (2, 1), (1, 2), (-1, 2), (-2, 1),
    (-2, -1), (-1, -2), (1, -2), (2, -1)
]

def count_options(grid, x, y, n):
    """Counts valid onward moves from a given square."""
    count = 0
    for dx, dy in DIR:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == -1:
            count += 1
    return count

def get_sorted_moves(grid, x, y, n):
    """Gets and sorts possible moves based on the number of onward options."""
    options = []
    for i, (dx, dy) in enumerate(DIR):
        nx, ny = x + dx, y + dy
        if 0 <= nx < n and 0 <= ny < n and grid[nx][ny] == -1:
            onward_moves = count_options(grid, nx, ny, n)
            options.append({'count': onward_moves, 'pos': (nx, ny)})
    options.sort(key=lambda m: m['count'])
    return [opt['pos'] for opt in options]

def knight_tour_util(grid, x, y, step, n):
    """Recursive utility to solve the Knight's Tour problem."""
    if step > n * n:
        return True

    moves = get_sorted_moves(grid, x, y, n)
    for nx, ny in moves:
        grid[nx][ny] = step
        if knight_tour_util(grid, nx, ny, step + 1, n):
            return True
        grid[nx][ny] = -1  # Backtrack
    return False

def solve_knight_tour(n, start_x, start_y):
    """Initializes and attempts to solve the tour from a starting point."""
    grid = np.full((n, n), -1, dtype=int)
    grid[start_x, start_y] = 1  # Start numbering from 1
    if knight_tour_util(grid, start_x, start_y, 2, n):
        return grid
    return None

# --- Streamlit UI and Visualization ---

st.set_page_config(layout="wide")

st.title("Knight's Tour Visualization")
st.write("An interactive web app to visualize the Knight's Tour using Python, Streamlit, and Matplotlib.")

# --- Session State Initialization ---
if 'tour_running' not in st.session_state:
    st.session_state.tour_running = False
if 'solution' not in st.session_state:
    st.session_state.solution = None
if 'path' not in st.session_state:
    st.session_state.path = None
if 'board_n' not in st.session_state:
    st.session_state.board_n = 5
if 'start_pos' not in st.session_state:
    st.session_state.start_pos = (0,0)


# --- Sidebar Controls ---
with st.sidebar:
    st.header("Controls")
    board_n = st.number_input("Board Size (N x N)", min_value=5, max_value=10, value=st.session_state.board_n, key="board_n_input")
    
    # Update board size if changed
    if board_n != st.session_state.board_n:
        st.session_state.board_n = board_n
        st.session_state.tour_running = False # Reset on size change

    st.session_state.start_pos = (
        st.number_input("Starting Row", 0, st.session_state.board_n - 1, st.session_state.start_pos[0]),
        st.number_input("Starting Column", 0, st.session_state.board_n - 1, st.session_state.start_pos[1])
    )
    
    speed_options = {"Slow": 0.5, "Medium": 0.2, "Fast": 0.05, "Instant": 0}
    selected_speed = st.select_slider("Animation Speed", options=list(speed_options.keys()), value="Medium")
    animation_speed = speed_options[selected_speed]

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Start Tour", use_container_width=True):
            st.session_state.tour_running = True
            st.session_state.solution = solve_knight_tour(st.session_state.board_n, st.session_state.start_pos[0], st.session_state.start_pos[1])
            if st.session_state.solution is not None:
                path = [None] * (st.session_state.board_n**2)
                for r in range(st.session_state.board_n):
                    for c in range(st.session_state.board_n):
                        path[st.session_state.solution[r, c] - 1] = (r, c)
                st.session_state.path = path
            else:
                 st.session_state.tour_running = False

    with col2:
        if st.button("Reset", use_container_width=True):
            st.session_state.tour_running = False
            st.session_state.solution = None
            st.session_state.path = None
            st.rerun()

# --- Main Board Display ---
progress_bar = st.progress(0)
progress_text = st.empty()
plot_placeholder = st.empty()

def draw_board(step):
    """Draws the chessboard and the knight's path up to the current step."""
    n = st.session_state.board_n
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.axis('off')

    # Draw chessboard
    for r in range(n):
        for c in range(n):
            color = "#d1d5db" if (r + c) % 2 == 0 else "#f9fafb"
            ax.add_patch(patches.Rectangle((c, r), 1, 1, facecolor=color))

    # Draw path if a solution exists
    if st.session_state.path:
        path = st.session_state.path
        for i in range(step):
            r, c = path[i]
            # Draw number
            ax.text(c + 0.5, r + 0.5, str(i + 1), ha='center', va='center', fontsize=16, color='#1e3a8a', weight='bold')
            # Draw arrow
            if i > 0:
                prev_r, prev_c = path[i - 1]
                ax.arrow(prev_c + 0.5, prev_r + 0.5, c - prev_c, r - prev_r,
                         head_width=0.2, head_length=0.3, fc='#2563eb', ec='#2563eb', length_includes_head=True)
    
    plot_placeholder.pyplot(fig)
    plt.close(fig)

# --- Animation Loop ---
if st.session_state.tour_running:
    if st.session_state.solution is None:
        st.error(f"No solution found starting from {st.session_state.start_pos}. Please try another starting point.")
        st.session_state.tour_running = False
    else:
        total_steps = st.session_state.board_n ** 2
        for i in range(total_steps):
            progress = (i + 1) / total_steps
            progress_bar.progress(progress)
            progress_text.text(f"Progress: {i + 1} / {total_steps}")
            draw_board(i + 1)
            if animation_speed > 0:
                time.sleep(animation_speed)
        progress_text.text(f"Tour Complete: {total_steps} / {total_steps}")
        st.session_state.tour_running = False # End of tour
else:
    # Show initial empty board
    n = st.session_state.board_n
    progress_bar.progress(0)
    progress_text.text(f"Progress: 0 / {n**2}")
    draw_board(0) # Draw an empty board

