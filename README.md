# Knight's Tour Visualization

This Streamlit application visualizes the Knight's Tour problem on a chessboard, utilizing Warnsdorff's Rule to find a solution. The application is designed to be fully responsive, providing an optimal user experience on both mobile and desktop devices.

## Features

* **Interactive Board Selection:** Click directly on the chessboard to select your desired starting position for the Knight's Tour.
* **Warnsdorff's Rule Implementation:** The algorithm prioritizes moves to squares with the fewest onward moves, increasing the likelihood of finding a closed tour.
* **Animated Visualization:** Watch the Knight traverse the board step-by-step with adjustable animation speeds.
* **Responsive Design:**
    * **Desktop:** Controls are displayed in a sidebar next to the board.
    * **Mobile:** Controls are collapsed into an expandable section, and the board takes full width for better viewing on smaller screens.
* **Dynamic Theming:** Automatically adapts to Streamlit's light or dark theme for a consistent look and feel.
* **Adjustable Board Size:** Solve the Knight's Tour on boards ranging from 5x5 to 10x10.

## How to Run Locally

Follow these steps to set up and run the application on your local machine.

### Prerequisites

* Python 3.10+
* `pip` (Python package installer)

### 1. Clone the Repository (if applicable)

If your code is in a Git repository, clone it:

```bash
git clone https://github.com/KeyCode17/knights-tour-challenge.git
cd https://github.com/KeyCode17/knights-tour-challenge.git
````

Otherwise, ensure `app.py` and `requirements.txt` are in the same directory.

### 2\. Create a Virtual Environment (Recommended)

It's good practice to use a virtual environment to manage dependencies:

```bash
python -m venv venv
```

### 3\. Activate the Virtual Environment

  * **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
  * **On macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

### 4\. Install Dependencies

Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

[cite\_start]*(Note: The `requirements.txt` specifies `streamlit==1.35.0`, `numpy==1.26.4`, `matplotlib==3.9.0`, `streamlit-image-coordinates==0.3.1`, `streamlit-screen-stats==0.0.82`, `streamlit-browser-session-storage==0.0.12`, and `streamlit-local-storage==0.0.25`[cite: 1].)*

### 5\. Run the Streamlit Application

```bash
streamlit run app.py
```

This command will open the application in your default web browser.

## Usage

1.  **Select Board Size:** Use the "Board Size" number input to choose a grid size between 5x5 and 10x10.
2.  **Choose Start Position:** Click directly on any square on the chessboard to set the starting position for the Knight.
3.  **Start the Tour:** Click the "Start" button to begin the animation of the Knight's Tour.
4.  **Adjust Speed:** Use the "Animation Speed" slider to control how fast the Knight moves across the board.
5.  **Reset:** Click the "Reset" button to clear the board and select a new starting position or board size.

## Project Structure

  * `app.py`: The main Streamlit application script containing the Knight's Tour algorithm, UI logic, and visualization.
  * `requirements.txt`: Lists all Python dependencies required to run the application.

## Algorithm Details

The Knight's Tour is solved using a backtracking algorithm enhanced with **Warnsdorff's Rule**. This heuristic helps to find a solution more efficiently by always moving the Knight to the square from which it has the fewest available onward moves. This strategy tends to keep the Knight away from "dead ends" on the board, making it more likely to complete the tour.

## Contributing

Feel free to fork the repository, make improvements, and submit pull requests.
