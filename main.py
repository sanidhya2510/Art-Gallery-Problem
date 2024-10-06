import tkinter as tk
from tkinter import messagebox
import generate_polygon as generate_polygon_module
import trapezoidalisation as trapezoidalisation_module
import monotone_partitioning as monotone_partitioning_module
import triangulation as triangulation_module
import dual_graph as dual_graph_module

# Function stubs for each button's functionality
def generate_polygon():
    global polygon_app  # Store the instance globally to access it later
    polygon_app = generate_polygon_module.GeneratePolygonApp(canvas)
    polygon_app.generate_polygon()
    polygon_app.dcel.display()

def trapezoidalisation():
    if polygon_app and polygon_app.dcel:  # Check if the polygon has been generated
        global trapezoidal_app
        trapezoidal_app = trapezoidalisation_module.TrapezoidalisationApp(canvas, polygon_app.dcel)
        trapezoidal_app.draw_trapezoidalisation()
    else:
        messagebox.showwarning("Warning", "Please generate a polygon first.")

def monotone_partitioning():
    if polygon_app and polygon_app.dcel:  # Check if the polygon has been generated
         global monotone_app 
         monotone_app = monotone_partitioning_module.MonotonePartitioningApp(canvas, polygon_app.dcel, trapezoidal_app)
         monotone_app.draw_monotone_partitioning()
    else:
        messagebox.showwarning("Warning", "Please generate a polygon first.")

def triangulation():
    if polygon_app and polygon_app.dcel:  # Check if the polygon has been generated
         global triangulation_app 
         triangulation_app = triangulation_module.TriangulationApp(canvas, polygon_app.dcel, monotone_app)
         triangulation_app.triangulate_polygon()
    else:
        messagebox.showwarning("Warning", "Please generate a polygon first.")

def dual_graph():
    if polygon_app and polygon_app.dcel:
        global dual_graph_App
        dual_graph_app = dual_graph_module.DualGraphApp(canvas, polygon_app.dcel, triangulation_app)
        dual_graph_app.create_dual_graph()
    else:
        messagebox.showwarning("Warning", "Please generate a polygon first. ")

def three_coloring():
    messagebox.showinfo("Action", "3 Coloring")

def vertex_guards():
    messagebox.showinfo("Action", "Vertex Guards")

# Main window setup
root = tk.Tk()
root.title("Geometry Operations")
root.geometry("800x600")  # Adjust the size to fit buttons and canvas

# Frame for the canvas (left side)
canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.LEFT, padx=20, pady=20)

# Create canvas where the polygon will be drawn
canvas = tk.Canvas(canvas_frame, width=500, height=500, bg="white")
canvas.pack()

# Frame to hold buttons (right side)
button_frame = tk.Frame(root)
button_frame.pack(side=tk.RIGHT, padx=20, pady=20)

# Create buttons
buttons = [
    ("Generate Polygon", generate_polygon),
    ("Trapezoidalisation", trapezoidalisation),
    ("Monotone Partitioning", monotone_partitioning),
    ("Triangulation", triangulation),
    ("Dual Graph", dual_graph),
    ("3 Coloring", three_coloring),
    ("Vertex Guards", vertex_guards)
]

# Adding buttons to the window
for btn_text, btn_command in buttons:
    button = tk.Button(button_frame, text=btn_text, width=20, command=btn_command)
    button.pack(pady=5)

# Initialize polygon_app as None
polygon_app = None

# Start the Tkinter event loop
root.mainloop()
