import time

class TriangulationApp:
    def __init__(self, canvas, dcel, monotone_app):
        self.canvas = canvas
        self.dcel = dcel
        self.monotone_app = monotone_app
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50  # Padding for the axes and graph
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding

    def triangulate_polygon(self):
        for face in self.dcel.faces:
            starting_vertex = face.outer_half_edge.origin
            