class VertexGuardsApp():
    def __init__(self, canvas, dcel, three_coloring_app):
        self.canvas = canvas
        self.dcel = dcel
        self.three_coloring_app = three_coloring_app
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding
        
    def decide_vertex_guards(self):
        y_count = 0
        g_count = 0
        p_count = 0

        yellow_vertices = []
        green_vertices = []
        pink_vertices = []

        self.canvas.delete('all')
        self.three_coloring_app.dual_graph_app.triangulation_app.monotone_app.trapezoidal_app.polygon_app.draw_axes()
        self.three_coloring_app.dual_graph_app.triangulation_app.monotone_app.trapezoidal_app.polygon_app.draw_polygon_without_delay()

        for k in self.three_coloring_app.colored_vertices:
            if self.three_coloring_app.colored_vertices[k] == "Yellow":
                y_count += 1
                yellow_vertices.append(k)
            elif self.three_coloring_app.colored_vertices[k] == "Green":
                g_count += 1
                green_vertices.append(k)
            else:
                p_count += 1
                pink_vertices.append(k)

        if y_count <= g_count and y_count <= p_count:
            min_color = "Yellow"
            min_color_vertices = yellow_vertices
        elif g_count <= p_count:
            min_color = "Green"
            min_color_vertices = green_vertices
        else:
            min_color = "Pink"
            min_color_vertices = pink_vertices
            
        for k in min_color_vertices:
            self.three_coloring_app.color_vertex(k, min_color)