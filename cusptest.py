import math

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

    def angle_between(self, v1, v2, v3):
        """Calculate the angle at v2 formed by v1 and v3, considering direction."""
        # Create vectors
        vec_a = (v1.x - v2.x, v1.y - v2.y)  # Vector from v2 to v1
        vec_b = (v3.x - v2.x, v3.y - v2.y)  # Vector from v2 to v3
        
        # Calculate the angle using atan2
        angle_a = math.atan2(vec_a[1], vec_a[0])  # Angle of vector a
        angle_b = math.atan2(vec_b[1], vec_b[0])  # Angle of vector b
        
        # Calculate the difference and normalize to [0, 360]
        angle_diff = math.degrees(angle_b - angle_a)
        if angle_diff < 0:
            angle_diff += 360
            
        return angle_diff  # Angle in degrees

    def find_vertices(self):
        start_vertices = []
        end_vertices = []
        min_cusp_vertices = []
        max_cusp_vertices = []

        for i, vertex in enumerate(self.vertices):
            prev_vertex = self.vertices[i - 1]  # Previous vertex
            next_vertex = self.vertices[(i + 1) % len(self.vertices)]  # Next vertex
            
            angle = self.angle_between(prev_vertex, vertex, next_vertex)

            # Check conditions for start vertex
            if (prev_vertex.y < vertex.y and next_vertex.y < vertex.y and angle > 180):
                start_vertices.append(vertex)
            
            # Check conditions for end vertex
            elif (prev_vertex.y > vertex.y and next_vertex.y > vertex.y and angle > 180):
                end_vertices.append(vertex)
                
            # Check conditions for min cusp vertex
            elif (prev_vertex.y < vertex.y and next_vertex.y < vertex.y and angle < 180):
                min_cusp_vertices.append(vertex)

            # Check conditions for max cusp vertex
            elif (prev_vertex.y > vertex.y and next_vertex.y > vertex.y and angle < 180):
                max_cusp_vertices.append(vertex)

        return {
            "start_vertices": start_vertices,
            "end_vertices": end_vertices,
            "min_cusp_vertices": min_cusp_vertices,
            "max_cusp_vertices": max_cusp_vertices,
        }

    def display(self):
        print("Vertices:")
        for vertex in self.vertices:
            print(f"({vertex.x}, {vertex.y})")

# Example Usage
if __name__ == "__main__":
    dcel = DCEL()
    # Use the provided points list representing a polygon
    points = [(0, 0), (50, 50), (100, 0), (150, 75), (100, 200), (50, 100), (25, 200)]
    dcel.construct_polygon(points)

    # Find and display the vertex types
    vertex_types = dcel.find_vertices()

    print("\nStart Vertices:")
    for vertex in vertex_types["start_vertices"]:
        print(f"({vertex.x}, {vertex.y})")
    
    print("\nEnd Vertices:")
    for vertex in vertex_types["end_vertices"]:
        print(f"({vertex.x}, {vertex.y})")
    
    print("\nMin Cusp Vertices:")
    for vertex in vertex_types["min_cusp_vertices"]:
        print(f"({vertex.x}, {vertex.y})")
    
    print("\nMax Cusp Vertices:")
    for vertex in vertex_types["max_cusp_vertices"]:
        print(f"({vertex.x}, {vertex.y})")
