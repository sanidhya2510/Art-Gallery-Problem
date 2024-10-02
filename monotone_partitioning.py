import time

class MonotonePartitioningApp:
    def __init__(self, canvas, dcel, trapezoidal_app):
        self.canvas = canvas
        self.dcel = dcel
        self.trapezoidal_app = trapezoidal_app
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50  # Padding for the axes and graph
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding

    def draw_monotone_partitioning(self):
        vertices = sorted(self.dcel.vertices, key=lambda v: v.y, reverse=True)  # Sort vertices top to bottom
        vertex_types = self.dcel.find_vertices()
        for vertex in vertices:
            self.trapezoidal_app.remove_horizontal_line(vertex)
            self.canvas.update()
            if vertex in vertex_types["min_cusp_vertices"]:
                self.handle_min_cusp(vertex)
            elif vertex in vertex_types["max_cusp_vertices"]:
                self.handle_max_cusp(vertex)
            
            time.sleep(0.4)  # Delay between each step for visualization

    def handle_min_cusp(self, vertex):
        """Handle downward cusps by connecting the vertex to the supporting vertex of the trapezoid below."""
        print("Processing min cusp:", vertex)
        supporting_vertex_below = self.find_supporting_vertex_below(vertex)
        
        if supporting_vertex_below:
            print("Connecting min cusp to supporting vertex below:", supporting_vertex_below)
            self.draw_diagonal(vertex, supporting_vertex_below)
        else:
            print("No supporting vertex below found for min cusp.")

    def handle_max_cusp(self, vertex):
        """Handle upward cusps by connecting the vertex to the supporting vertex of the trapezoid above."""
        print("Processing max cusp:", vertex)
        supporting_vertex_above = self.find_supporting_vertex_above(vertex)
        
        if supporting_vertex_above:
            print("Connecting max cusp to supporting vertex above:", supporting_vertex_above)
            self.draw_diagonal(vertex, supporting_vertex_above)
        else:
            print("No supporting vertex above found for max cusp.")

    def find_supporting_vertex_below(self, vertex):
        """Find the supporting vertex of the trapezoid below the current vertex."""
        vertices_below = sorted([v for v in self.dcel.vertices if v.y < vertex.y], key=lambda v: v.y, reverse=True)
        
        for v in vertices_below:
            if self.is_visible(vertex, v):
                return v  # Return the first visible vertex below
        return None

    def find_supporting_vertex_above(self, vertex):
        """Find the supporting vertex of the trapezoid above the current vertex."""
        vertices_above = sorted([v for v in self.dcel.vertices if v.y > vertex.y], key=lambda v: v.y)

        for v in vertices_above:
            if self.is_visible(vertex, v):
                return v  # Return the first visible vertex above
        return None

    def is_visible(self, vertex1, vertex2):
        """Check if the line segment from vertex1 to vertex2 intersects with any edges of the polygon."""
        for i in range(len(self.dcel.vertices)):
            start_vertex = self.dcel.vertices[i]
            end_vertex = self.dcel.vertices[(i + 1) % len(self.dcel.vertices)]
            
            # Only check for intersection if the segments are not the same
            if (vertex1 != start_vertex and vertex1 != end_vertex and
                vertex2 != start_vertex and vertex2 != end_vertex):
                if self.segments_intersect(vertex1, vertex2, start_vertex, end_vertex):
                    return False  # They intersect, so they are not visible
        return True  # They are visible

    def segments_intersect(self, p1, p2, p3, p4):
        """Return True if the line segments p1p2 and p3p4 intersect."""
        def orientation(p, q, r):
            """Return the orientation of the ordered triplet (p, q, r)."""
            val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if val == 0:
                return 0
            return 1 if val > 0 else 2
        
        def on_segment(p, q, r):
            """Check if point q lies on segment pr."""
            return (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and
                    q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y))

        o1 = orientation(p1, p2, p3)
        o2 = orientation(p1, p2, p4)
        o3 = orientation(p3, p4, p1)
        o4 = orientation(p3, p4, p2)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special Cases
        if o1 == 0 and on_segment(p1, p3, p2):
            return True
        if o2 == 0 and on_segment(p1, p4, p2):
            return True
        if o3 == 0 and on_segment(p3, p1, p4):
            return True
        if o4 == 0 and on_segment(p3, p2, p4):
            return True

        return False

    def draw_diagonal(self, vertex1, vertex2):
        """Draw a diagonal line connecting two vertices and update the DCEL structure."""
        x1, y1 = vertex1.x, vertex1.y
        x2, y2 = vertex2.x, vertex2.y

        # Adjust coordinates to fit within the positive axes
        adjusted_x1 = self.origin_x + x1
        adjusted_y1 = self.origin_y - y1
        adjusted_x2 = self.origin_x + x2
        adjusted_y2 = self.origin_y - y2

        # Draw the diagonal on the canvas
        self.canvas.create_line(adjusted_x1, adjusted_y1, adjusted_x2, adjusted_y2, fill="red")

        # Update DCEL: Add a new half-edge for the diagonal
        self.dcel.add_diagonal(vertex1, vertex2)
        
