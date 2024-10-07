class ThreeColoringApp():
    def __init__(self, canvas, dcel, dual_graph_app):
        self.canvas = canvas
        self.dcel = dcel
        self.dual_graph_app = dual_graph_app
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding
        self.colors = ["brown", "yellow", "green"]
    
    def three_color_triangulation(self):
        # Store colors of vertices
        vertex_colors = {}

        # Get the centroids and edges from the dual graph
        centroids = self.dual_graph_app.get_centroids()

        # Start with the first face in the triangulation and assign colors to its vertices
        first_face = list(self.dcel.faces)[0]
        if first_face.outer_half_edge:
            vertices = self.get_face_vertices(first_face)
            # Assign three different colors to the vertices of the first triangle
            for i, vertex in enumerate(vertices):
                vertex_colors[vertex] = self.colors[i % 3]
                self.color_vertex(vertex, vertex_colors[vertex])

        # Now traverse the dual graph to color the rest of the triangulation
        for face in self.dcel.faces:
            if face.outer_half_edge:
                half_edge = face.outer_half_edge
                start_edge = half_edge
                # Traverse the edges of each face (triangle)
                while True:
                    twin_edge = half_edge.twin
                    if twin_edge and twin_edge.incident_face and twin_edge.incident_face != first_face:
                        # Get the common edge's vertices
                        common_vertices = self.get_common_edge_vertices(half_edge)
                        if common_vertices:
                            # Get the uncolored vertex of the adjacent triangle
                            uncolored_vertex = self.get_uncolored_vertex(twin_edge.incident_face, vertex_colors)
                            if uncolored_vertex:
                                # Assign the third color (the one not used by the common edge)
                                used_colors = {vertex_colors[common_vertices[0]], vertex_colors[common_vertices[1]]}
                                uncolored_vertex_color = next(color for color in self.colors if color not in used_colors)
                                vertex_colors[uncolored_vertex] = uncolored_vertex_color
                                self.color_vertex(uncolored_vertex, uncolored_vertex_color)

                    half_edge = half_edge.next
                    if half_edge == start_edge:
                        break

    def get_face_vertices(self, face):
        """Get the vertices of a given face."""
        vertices = []
        half_edge = face.outer_half_edge
        start_edge = half_edge
        while True:
            vertices.append(half_edge.origin)
            half_edge = half_edge.next
            if half_edge == start_edge:
                break
        return vertices

    def get_common_edge_vertices(self, half_edge):
        """Get the vertices of a common edge between two triangles."""
        return [half_edge.origin, half_edge.next.origin]

    def get_uncolored_vertex(self, face, vertex_colors):
        """Find the uncolored vertex in a given triangle."""
        vertices = self.get_face_vertices(face)
        for vertex in vertices:
            if vertex not in vertex_colors:
                return vertex
        return None

    def color_vertex(self, vertex, color):
        """Draw the vertex with the given color."""
        adjusted_x = self.origin_x + vertex.x
        adjusted_y = self.origin_y - vertex.y
        self.canvas.create_oval(adjusted_x - 5, adjusted_y - 5, adjusted_x + 5, adjusted_y + 5, fill=color)    
    