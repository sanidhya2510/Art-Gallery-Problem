import tkinter as tk
from tkinter import messagebox
import generate_polygon as generate_polygon_module
import trapezoidalisation as trapezoidalisation_module
import monotone_partitioning as monotone_partitioning_module
import triangulation as triangulation_module
import dual_graph as dual_graph_module
import three_coloring as three_coloring_module
import vertex_guards as vertex_guards_module

def update_button_states(next_button=None):
    trapezoidal_btn.config(state=tk.DISABLED)
    monotone_btn.config(state=tk.DISABLED)
    triangulation_btn.config(state=tk.DISABLED)
    dual_graph_btn.config(state=tk.DISABLED)
    coloring_btn.config(state=tk.DISABLED)
    vertex_guards_btn.config(state=tk.DISABLED)
    
    generate_polygon_btn.config(state=tk.NORMAL)

    if next_button:
        next_button.config(state=tk.NORMAL)

def generate_polygon():
    global polygon_app  
    polygon_app = generate_polygon_module.GeneratePolygonApp(canvas)
    polygon_app.generate_polygon()
    polygon_app.dcel.display()
    update_button_states(trapezoidal_btn)

def trapezoidalisation():
    if polygon_app and polygon_app.dcel:  
        global trapezoidal_app
        trapezoidal_app = trapezoidalisation_module.TrapezoidalisationApp(canvas, polygon_app.dcel, polygon_app)
        trapezoidal_app.draw_trapezoidalisation()
        update_button_states(monotone_btn)
    else:
        messagebox.showwarning("Warning", "Please generate a polygon first.")

def monotone_partitioning():
    if polygon_app and polygon_app.dcel:  
        global monotone_app 
        monotone_app = monotone_partitioning_module.MonotonePartitioningApp(canvas, polygon_app.dcel, trapezoidal_app)
        monotone_app.draw_monotone_partitioning()
        update_button_states(triangulation_btn)
    else:
        messagebox.showwarning("Warning", "Please generate a polygon first.")

def triangulation():
    if polygon_app and polygon_app.dcel:  
        global triangulation_app 
        triangulation_app = triangulation_module.TriangulationApp(canvas, polygon_app.dcel, monotone_app)
        triangulation_app.triangulate_polygon()
        update_button_states(dual_graph_btn)
    else:
        messagebox.showwarning("Warning", "Please generate a polygon first.")

def dual_graph():
    if polygon_app and polygon_app.dcel:
        global dual_graph_app
        dual_graph_app = dual_graph_module.DualGraphApp(canvas, polygon_app.dcel, triangulation_app)
        dual_graph_app.create_dual_graph()
        update_button_states(coloring_btn)
    else:
        messagebox.showwarning("Warning", "Please generate a polygon first.")

def three_coloring():
    if polygon_app and polygon_app.dcel:
        global three_coloring_app
        three_coloring_app = three_coloring_module.ThreeColoringApp(canvas, polygon_app.dcel, dual_graph_app)
        three_coloring_app.three_color_triangulation()
        update_button_states(vertex_guards_btn)
    else:
        messagebox.showwarning("Warning", "Please generate a polygon first.")  

def vertex_guards():
    if polygon_app and polygon_app.dcel:
        global vertex_guards_app
        vertex_guards_app = vertex_guards_module.VertexGuardsApp(canvas, polygon_app.dcel, three_coloring_app)
        vertex_guards_app.decide_vertex_guards()
        update_button_states()
    else:
        messagebox.showwarning("Warning", "Please generate a polygon first.")  

root = tk.Tk()
root.title("Art Gallery Problem")
root.geometry("800x600")

canvas_frame = tk.Frame(root)
canvas_frame.pack(side=tk.LEFT, padx=20, pady=20)

canvas = tk.Canvas(canvas_frame, width=500, height=500, bg="white")
canvas.pack()

button_frame = tk.Frame(root)
button_frame.pack(side=tk.RIGHT, padx=20, pady=20)

generate_polygon_btn = tk.Button(button_frame, text="Generate Polygon", width=20, command=generate_polygon)
generate_polygon_btn.pack(pady=5)

trapezoidal_btn = tk.Button(button_frame, text="Trapezoidalisation", width=20, command=trapezoidalisation, state=tk.DISABLED)
trapezoidal_btn.pack(pady=5)

monotone_btn = tk.Button(button_frame, text="Monotone Partitioning", width=20, command=monotone_partitioning, state=tk.DISABLED)
monotone_btn.pack(pady=5)

triangulation_btn = tk.Button(button_frame, text="Triangulation", width=20, command=triangulation, state=tk.DISABLED)
triangulation_btn.pack(pady=5)

dual_graph_btn = tk.Button(button_frame, text="Dual Graph", width=20, command=dual_graph, state=tk.DISABLED)
dual_graph_btn.pack(pady=5)

coloring_btn = tk.Button(button_frame, text="3 Coloring", width=20, command=three_coloring, state=tk.DISABLED)
coloring_btn.pack(pady=5)

vertex_guards_btn = tk.Button(button_frame, text="Vertex Guards", width=20, command=vertex_guards, state=tk.DISABLED)
vertex_guards_btn.pack(pady=5)

polygon_app = None

root.mainloop()
