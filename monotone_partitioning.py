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
        for vertex in vertices:
            # Check if the vertex is an interior cusp
            is_cusp, cusp_type = self.check_if_cusp(vertex)
            if is_cusp:
                print("cusp")
                # Handle minimum cusp (downward cusp)
                if cusp_type == 'min':
                    self.handle_min_cusp(vertex)

                # Handle maximum cusp (upward cusp)
                elif cusp_type == 'max':
                    self.handle_max_cusp(vertex)

            time.sleep(0.4)  # Delay between each step for visualization

    def check_if_cusp(self, vertex):
        incident_edge = vertex.incident_half_edge
        if incident_edge is None:
            return False, None  # Not a cusp if no incident edge

        prev_vertex = incident_edge.twin.next.destination if incident_edge.twin else None
        next_vertex = incident_edge.next.destination if incident_edge.next else None

        if prev_vertex and next_vertex:
            # Check if the vertex forms an upward cusp (max) or downward cusp (min)
            if prev_vertex.y > vertex.y and next_vertex.y > vertex.y:
                return True, 'min'
            elif prev_vertex.y < vertex.y and next_vertex.y < vertex.y:
                return True, 'max'

        return False, None


    def handle_min_cusp(self, vertex):
        """Handle downward cusps by connecting the vertex to the supporting vertex of the trapezoid below."""
        print("min")
        supporting_vertex_below = self.find_supporting_vertex_below(vertex)
        
        if supporting_vertex_below:
            # Draw a new diagonal connecting the current vertex to the supporting vertex below
            self.draw_diagonal(vertex, supporting_vertex_below)

    def handle_max_cusp(self, vertex):
        print("max")
        """Handle upward cusps by connecting the vertex to the supporting vertex of the trapezoid above."""
        supporting_vertex_above = self.find_supporting_vertex_above(vertex)
        
        if supporting_vertex_above:
            # Draw a new diagonal connecting the current vertex to the supporting vertex above
            self.draw_diagonal(vertex, supporting_vertex_above)

    def find_supporting_vertex_below(self, vertex):
        """Find the supporting vertex of the trapezoid below the current vertex."""
        vertices_below = [v for v in self.dcel.vertices if v.y < vertex.y]
        if vertices_below:
            return max(vertices_below, key=lambda v: v.y)  # Return the highest vertex below
        return None

    def find_supporting_vertex_above(self, vertex):
        """Find the supporting vertex of the trapezoid above the current vertex."""
        vertices_above = [v for v in self.dcel.vertices if v.y > vertex.y]
        if vertices_above:
            return min(vertices_above, key=lambda v: v.y)  # Return the lowest vertex above
        return None

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
