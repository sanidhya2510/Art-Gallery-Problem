
# Art Gallery Problem Visualization

This project provides a visual implementation of several computational geometry algorithms, particularly focusing on the **Art Gallery Problem**. The application allows you to generate polygons and apply various algorithms such as trapezoidal decomposition, monotone partitioning, triangulation, dual graph generation, vertex guards computation, and more.

## Directory Structure

```
|-- ART-GALLERY-PROBLEM-MAIN/
    |-- __pycache__/
    |-- dcel.py
    |-- dual_graph.py
    |-- generate_polygon.py
    |-- main.py
    |-- monotone_partitioning.py
    |-- README.md
    |-- three_coloring.py
    |-- trapezoidalisation.py
    |-- triangulation.py
    |-- vertex_guards.py
```

### File Descriptions

- **`dcel.py`**: Implements a doubly connected edge list (DCEL) data structure for polygon representation.
- **`dual_graph.py`**: Contains functions related to dual graph generation from polygonal decompositions.
- **`generate_polygon.py`**: Provides functionality to generate random or user-defined polygons.
- **`main.py`**: The main entry point for the program. It manages the user interface and the interaction between different algorithms.
- **`monotone_partitioning.py`**: Implements monotone partitioning algorithms to break polygons into simpler monotone pieces.
- **`three_coloring.py`**: Implements a three-coloring algorithm for triangulated polygons.
- **`trapezoidalisation.py`**: Contains the implementation of the trapezoidal decomposition of a polygon.
- **`triangulation.py`**: Provides triangulation algorithms for polygons.
- **`vertex_guards.py`**: Implements algorithms to determine the minimal number of vertex guards needed for art gallery problems.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8+
- Tkinter (for GUI)
If Tkinter is not installed, you can install it via:

```bash
sudo apt-get install python3-tk
```

or for Windows:

```bash
pip install tk
```

## How to Run the Project

To run the main file, follow these steps:

1. Clone the repository or download the files into a folder:

```bash
git clone https://github.com/sanidhya2510/Art-Gallery-Problem
cd art-gallery-problem
```

2. (Optional) Create a virtual environment and activate it:

```bash
# For Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
```

3. Install any necessary dependencies (if applicable):

```bash
pip install -r requirements.txt
```

4. Run the main program:

```bash
python main.py
```

## Usage

Once the GUI window opens, you can:

- **Generate Polygon**: Create a new polygon to apply algorithms on.
- **Trapezoidal Decomposition**: Decompose the polygon into trapezoids.
- **Monotone Partitioning**: Partition the polygon into monotone pieces.
- **Triangulation**: Triangulate the polygon.
- **Dual Graph Generation**: Create a dual graph from the decomposition.
- **Three Coloring**: Apply a three-coloring algorithm to the triangulated polygon.
- **Vertex Guards**: Calculate the minimal number of vertex guards needed.

## License

This project is licensed under the MIT License.

---
