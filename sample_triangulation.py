class HalfEdge:
    def __init__(self, origin=None):
        self.origin = origin  # Vertex where the half-edge originates
        self.next = None      # Next half-edge in the face
        self.prev = None      # Previous half-edge in the face
        self.twin = None      # Twin half-edge
        self.face = None      # Face to which this half-edge belongs

class Vertex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.incident_edge = None  # One of the half-edges originating from this vertex

class Face:
    def __init__(self):
        self.outer_edge = None      # An arbitrary edge of the face
        self.inner_edges = []       # List of inner edges for holes

class DCEL:
    def __init__(self, vertices):
        self.vertices = []
        self.edges = []
        self.faces = []
        self.create_dcel(vertices)

    def create_dcel(self, vertices):
        # Create vertices and half-edges from the ordered list
        for x, y in vertices:
            vertex = Vertex(x, y)
            self.vertices.append(vertex)

        # Create half-edges and link them
        n = len(self.vertices)
        for i in range(n):
            half_edge = HalfEdge(self.vertices[i])
            self.edges.append(half_edge)
            if i > 0:
                self.edges[i-1].next = half_edge  # Link previous edge to current
                half_edge.prev = self.edges[i-1]  # Set the previous edge of current

        # Complete the circular link
        self.edges[n-1].next = self.edges[0]
        self.edges[0].prev = self.edges[n-1]

        # Set the outer face
        face = Face()
        self.faces.append(face)
        face.outer_edge = self.edges[0]  # First edge is the outer edge
        for edge in self.edges:
            edge.face = face

def is_counter_clockwise(v1, v2, v3):
    return (v2.x - v1.x) * (v3.y - v1.y) - (v3.x - v1.x) * (v2.y - v1.y) > 0

def triangulate_y_monotone_polygon(dcel):
    triangles = []
    vertex_stack = []

    # Start with the first edge
    start_edge = dcel.faces[0].outer_edge
    current_edge = start_edge

    # Populate the vertex stack in the order they appear around the polygon
    while True:
        vertex_stack.append(current_edge.origin)
        current_edge = current_edge.next
        if current_edge == start_edge:
            break

    # Process the vertices to create triangles
    while len(vertex_stack) > 2:
        v1 = vertex_stack[-3]
        v2 = vertex_stack[-2]
        v3 = vertex_stack[-1]

        # Check for the orientation
        if is_counter_clockwise(v1, v2, v3):
            triangles.append((v1, v2, v3))
            vertex_stack.pop(-2)  # Remove the middle vertex to form a triangle
        else:
            vertex_stack.pop()  # Remove the last vertex

    # Check if there are any remaining vertices and form the last triangle
    while len(vertex_stack) > 2:
        v1 = vertex_stack.pop()   # Pop last vertex
        v2 = vertex_stack[-1]     # Get the new last vertex
        v3 = vertex_stack[-2]     # Get the new second last vertex
        triangles.append((v1, v2, v3))  # Add the triangle formed by these vertices

    return triangles

# Example usage
def main():
    # Specify vertices of the y-monotone polygon in ordered form
    vertices = [(50, 0), (100, 50), (75, 75), (100, 100), (50, 150), (0, 100), (25, 75), (0, 50)]
    
    # Create the DCEL from the given vertices
    dcel = DCEL(vertices)
    
    # Perform triangulation
    triangles = triangulate_y_monotone_polygon(dcel)

    # Output the resulting triangles
    for triangle in triangles:
        print(f"Triangle: ({triangle[0].x}, {triangle[0].y}), "
              f"({triangle[1].x}, {triangle[1].y}), "
              f"({triangle[2].x}, {triangle[2].y})")

if __name__ == "__main__":
    main()
