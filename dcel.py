class Vertex:
    def __init__(self, x, y):
        self.x = x  # X-coordinate
        self.y = y  # Y-coordinate
        self.incident_half_edge = None  # Pointer to an incident half-edge


class HalfEdge:
    def __init__(self, origin):
        self.origin = origin  # The vertex at the start of this half-edge
        self.twin = None      # Pointer to the twin half-edge
        self.next = None      # Pointer to the next half-edge in the face
        self.face = None      # Pointer to the face this half-edge belongs to
        
    def destination(self):
        return self.next.origin if self.next else None


class Face:
    def __init__(self):
        self.outer_half_edge = None  # Pointer to one of the half-edges of the face


class DCEL:
    def __init__(self):
        self.vertices = []  # List to store all vertices
        self.half_edges = []  # List to store all half-edges
        self.faces = []  # List to store all faces

    def add_vertex(self, x, y):
        vertex = Vertex(x, y)
        self.vertices.append(vertex)
        return vertex

    def add_half_edge(self, origin):
        half_edge = HalfEdge(origin)
        self.half_edges.append(half_edge)
        return half_edge

    def add_face(self):
        face = Face()
        self.faces.append(face)
        return face

    def connect_half_edges(self, half_edge1, half_edge2):
        half_edge1.next = half_edge2  # Connect the next pointers of half-edges
        half_edge2.twin = half_edge1  # Set twin pointers

    def construct_polygon(self, points):
        # Create vertices for each point
        vertex_list = [self.add_vertex(x, y) for x, y in points]

        # Create half-edges and connect them
        for i in range(len(vertex_list)):
            he1 = self.add_half_edge(vertex_list[i])  # Outgoing half-edge from vertex i
            he2 = self.add_half_edge(vertex_list[(i + 1) % len(vertex_list)])  # Outgoing half-edge to vertex i+1
            self.connect_half_edges(he1, he2)  # Connect half-edges

            # Set the incident half-edge for the vertices
            vertex_list[i].incident_half_edge = he1

        # Create a face for the polygon
        face = self.add_face()
        face.outer_half_edge = vertex_list[0].incident_half_edge  # Assign the outer half-edge to the face

        # Set the face pointer for the half-edges
        for he in self.half_edges:
            he.face = face

    def display(self):
        print("Vertices:")
        for vertex in self.vertices:
            print(f"({vertex.x}, {vertex.y})")

        print("\nHalf-Edges:")
        for half_edge in self.half_edges:
            print(f"Origin: ({half_edge.origin.x}, {half_edge.origin.y})")

        print("\nFaces:")
        for face in self.faces:
            print("Face with outer half-edge starting at:", face.outer_half_edge.origin)


# Example Usage
if __name__ == "__main__":
    dcel = DCEL()
    # Example points representing a simple polygon (in this case, a triangle)
    points = [(0, 0), (100, 0), (50, 50)]
    dcel.construct_polygon(points)
    dcel.display()
