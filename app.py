import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import numpy as np
from streamlit_image_coordinates import streamlit_image_coordinates
from io import BytesIO
from PIL import Image
from st_screen_stats import ScreenData

# Use a single, centered layout for the page configuration.
st.set_page_config(
    layout="centered",
    page_title="Knight's Tour Challenge",  # Changes the browser tab title
    page_icon="🐴",
)
screenD = ScreenData(setTimeout=1000)
screen_d = screenD.st_screen_data()

# Check if screen_d is not None and the key exists before accessing it.
if screen_d and "innerWidth" in screen_d:
    device_width = screen_d["innerWidth"]
else:
    # Set a default value if screen data isn't available yet.
    device_width = 0

# --- Dynamic Theme-Aware Color Palettes ---

# Define color palettes for both light and dark themes.
light_theme_colors = {
    "light_square": "#f0f2f6",  # Light gray for light squares
    "dark_square": "#bdbdbd",    # Darker gray for dark squares
    "number_color": "#1e3a8a",  # Deep blue for text
    "arrow_color": "#2563eb",   # Vibrant blue for arrows
    "start_highlight": "#d32f2f" # Red to highlight the start square
}

dark_theme_colors = {
    "light_square": "#262730",  # Dark gray for light squares
    "dark_square": "#4c4e5a",   # Lighter dark gray for dark squares
    "number_color": "#79b8f5",  # Light blue for text
    "arrow_color": "#529ef8",   # Brighter blue for arrows
    "start_highlight": "#ef5350" # Lighter red for dark mode
}

theme_base = st.get_option("theme.base")
if theme_base == "dark":
    colors = dark_theme_colors
else:
    colors = light_theme_colors


# --- Knight's Tour Algorithm (Warnsdorff's rule) ---
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

st.title("Knight's Tour Visualization")
st.write("Select a starting square by clicking directly on the board.")
progress_bar = st.progress(0)
progress_text = st.empty()

# --- Session State Initialization ---
# Initialize state variables if they don't exist
if 'tour_running' not in st.session_state:
    st.session_state.tour_running = False
if 'solution' not in st.session_state:
    st.session_state.solution = None
if 'path' not in st.session_state:
    st.session_state.path = None
if 'board_n' not in st.session_state:
    st.session_state.board_n = 5
if 'start_pos' not in st.session_state:
    st.session_state.start_pos = (0, 0)
if 'fig_size_px' not in st.session_state:
    st.session_state.fig_size_px = 400
if "board_n" not in st.session_state:
    st.session_state.board_n = 5

# --- Render Controls ---
def render_controls():
    """Renders all the control widgets."""
    st.header("Controls")
    # Get the current value from session state
    current_board_n = st.session_state.board_n
    
    # Ensure the value is within the min/max range before passing it
    if current_board_n < 5:
        current_board_n = 5
    elif current_board_n > 10:
        current_board_n = 10
    
    board_n = st.number_input("Board Size", min_value=5, max_value=10,
                              value=current_board_n, key="board_n_input")

    if board_n != st.session_state.board_n:
        st.session_state.board_n = board_n
        st.session_state.tour_running = False
        st.session_state.solution = None
        st.session_state.path = None
        st.session_state.start_pos = (0, 0)
        st.rerun()
        
    if device_width > 0 and device_width < 650:
        pass
    else:
        display_pos = tuple(x + 1 for x in st.session_state.start_pos)
        st.caption(f"Selected Start: `{display_pos}`")
        st.divider()

    speed_options = {"Slow": 0.5, "Medium": 0.2, "Fast": 0.05, "Fastest": 0}
    selected_speed = st.select_slider("Animation Speed", options=list(speed_options.keys()), value="Medium")
    animation_speed = speed_options[selected_speed] # This will be used later
    st.session_state.animation_speed = animation_speed # Store in session state

# --- Render Play ---
def play_button():
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Start", use_container_width=True, type="primary", disabled=st.session_state.tour_running):
            st.session_state.tour_running = True
            with st.spinner("Calculating tour..."):
                st.session_state.solution = solve_knight_tour(st.session_state.board_n, st.session_state.start_pos[0], st.session_state.start_pos[1])

            if st.session_state.solution is not None:
                path = [None] * (st.session_state.board_n**2)
                for r in range(st.session_state.board_n):
                    for c in range(st.session_state.board_n):
                        path[st.session_state.solution[r, c] - 1] = (r, c)
                st.session_state.path = path
            else:
                st.session_state.tour_running = False
            st.rerun()

    with c2:
        if st.button("Reset", use_container_width=True):
            st.session_state.tour_running = False
            st.session_state.solution = None
            st.session_state.path = None
            st.session_state.start_pos = (0, 0)
            st.rerun()

# --- Responsive Layout --
if device_width < 650:
    # --- Mobile Layout ---
    with st.expander("Show Controls", expanded=False):
        render_controls() # Place all controls inside the expander
    play_button()
    display_pos = tuple(x + 1 for x in st.session_state.start_pos)
    st.divider()
    st.caption(f"Selected Start: `{display_pos}`")
    plot_placeholder = st.empty()
else:
    # --- Desktop Layout ---
    col_left, col_center = st.columns([1, 2])
    with col_left:
        render_controls() # Place controls in the left column
        st.divider()
        play_button()
    with col_center:
        plot_placeholder = st.empty() # The plot goes in the right column

def draw_board(step, board_colors, is_interactive=False):
    """
    Draws the chessboard and path.
    - If is_interactive, returns a PIL Image object for streamlit_image_coordinates.
    - Otherwise, returns a Matplotlib Figure object for st.pyplot.
    """
    n = st.session_state.board_n
    dpi = 100
    fig_size_inches = st.session_state.fig_size_px / dpi
    fig, ax = plt.subplots(figsize=(fig_size_inches, fig_size_inches), dpi=dpi)

    ax.set_xlim(0, n)
    ax.set_ylim(0, n)
    ax.set_aspect('equal')
    ax.invert_yaxis()
    ax.axis('off')

    # Draw chessboard
    for r in range(n):
        for c in range(n):
            color = board_colors["dark_square"] if (r + c) % 2 == 0 else board_colors["light_square"]
            ax.add_patch(patches.Rectangle((c, r), 1, 1, facecolor=color))

    # Highlight the selected start position on the interactive board
    if is_interactive:
        start_r, start_c = st.session_state.start_pos
        ax.add_patch(patches.Rectangle((start_c, start_r), 1, 1,
                                     edgecolor=board_colors["start_highlight"], facecolor='none', lw=4))
        ax.text(start_c + 0.5, start_r + 0.5, "★", ha='center', va='center',
                fontsize=20, color=board_colors["start_highlight"])

    # Draw path if a solution exists and it's not the interactive selection board
    if st.session_state.path and not is_interactive:
        path = st.session_state.path
        for i in range(step):
            r, c = path[i]
            # Draw number
            ax.text(c + 0.5, r + 0.5, str(i + 1), ha='center', va='center',
                    fontsize=16, color=board_colors["number_color"], weight='bold')
            # Draw arrow
            if i > 0:
                prev_r, prev_c = path[i - 1]
                ax.arrow(prev_c + 0.5, prev_r + 0.5, c - prev_c, r - prev_r,
                         head_width=0.2, head_length=0.3,
                         fc=board_colors["arrow_color"], ec=board_colors["arrow_color"],
                         length_includes_head=True)

    # If the board is for the interactive selector, convert to an image.
    if is_interactive:
        img_buffer = BytesIO()
        fig.savefig(img_buffer, format="png", bbox_inches='tight', pad_inches=0)
        plt.close(fig)  # Close the figure, we are done with it.
        img_buffer.seek(0)
        image = Image.open(img_buffer)
        return image
    # Otherwise, return the figure object directly for st.pyplot.
    else:
        return fig

# --- Animation Loop & Interactive Board ---
if st.session_state.tour_running:
    if st.session_state.solution is None:
        st.error(f"No solution found starting from {st.session_state.start_pos}. Please reset and try again.")
        st.session_state.tour_running = False
    else:
        total_steps = st.session_state.board_n ** 2
        for i in range(total_steps):
            progress = (i + 1) / total_steps
            progress_bar.progress(progress)
            progress_text.text(f"Progress: {i + 1} / {total_steps}")

            # 1. Get the Matplotlib figure object directly.
            board_fig = draw_board(i + 1, colors, is_interactive=False)
            
            # 2. Render the figure using st.pyplot into the placeholder.
            #    This will now work correctly on both desktop and mobile.
            plot_placeholder.pyplot(board_fig, use_container_width=True)

            # 3. CRITICAL: Close the figure to free up memory.
            plt.close(board_fig)

            if st.session_state.animation_speed > 0:
                time.sleep(st.session_state.animation_speed)

        progress_text.text(f"Tour Complete: {total_steps} / {total_steps}")
        st.session_state.tour_running = False
else:
    # --- INTERACTIVE BOARD (This part remains unchanged and works as intended) ---
    n = st.session_state.board_n
    progress_bar.progress(0)
    progress_text.text(f"Progress: 0 / {n**2}")

    # This call correctly gets the PIL Image because is_interactive=True
    interactive_board_img = draw_board(0, colors, is_interactive=True)

    with plot_placeholder:
        value = streamlit_image_coordinates(interactive_board_img, key="coords", use_column_width="always")

        if value:
            img_width = value["width"]
            img_height = value["height"]
            square_width = img_width / n
            square_height = img_height / n
            col = int(value["x"] / square_width)
            row = int(value["y"] / square_height)
            if 0 <= row < n and 0 <= col < n:
                if st.session_state.start_pos != (row, col):
                    st.session_state.start_pos = (row, col)
                    st.rerun()
