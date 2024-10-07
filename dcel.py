import math

class Vertex:
    def __init__(self, x, y):
        self.x = x  
        self.y = y 
        self.incident_half_edges = [] 
        self.incident_edges_and_faces = []

class HalfEdge:
    def __init__(self):
        self.origin = None
        self.twin = None  
        self.next = None  
        self.incident_face = None   
        self.prev = None
        self.target = None

class Face:
    def __init__(self):
        self.outer_half_edge = None 
        self.number = 0

class DCEL:
    def __init__(self):
        self.vertices = []  
        self.half_edges = []  
        self.faces = []  

    def add_vertex(self, x, y):
        vertex = Vertex(x, y)
        self.vertices.append(vertex)
        return vertex

    def add_edge(self, v1, v2):
        half_edge1 = HalfEdge()
        half_edge2 = HalfEdge()
        
        half_edge1.twin = half_edge2
        half_edge2.twin = half_edge1
        
        half_edge1.origin = v1
        half_edge2.origin = v2
        half_edge1.target = v2
        half_edge2.target = v1
        
        v1.incident_half_edges.append(half_edge1)
        v2.incident_half_edges.append(half_edge2)
        
        self.half_edges.append(half_edge1)
        self.half_edges.append(half_edge2)
        
        return half_edge1, half_edge2

    def add_face(self, outer_half_edge):
        face = Face()
        face.outer_half_edge = outer_half_edge
        
        edge = outer_half_edge
        while True:
            edge.target.incident_edges_and_faces.append((face, edge))
            edge.incident_face = face
            edge = edge.next
            if edge == outer_half_edge:
                break
            
        self.faces.append(face)
    
    def add_diagonal(self, v1, v2):
        common_face_list = []
        for x in v1.incident_edges_and_faces:
            for y in v2.incident_edges_and_faces:
                if x[0] is not None and y[0] is not None:
                    if x[0] == y[0]:
                        common_face_list.append(x)
                        common_face_list.append(y)
                        break
        
        common_face = common_face_list[0][0]
        temp_half_edge = common_face_list[0][1]
        half_edge1, half_edge2 = self.add_edge(v1, v2)
        half_edge2.next = temp_half_edge.next
        half_edge2.next.prev = half_edge2
        half_edge1.prev = temp_half_edge
        temp_half_edge.next = half_edge1
       
        new_face1 = Face()
        new_face2 = Face()
        
        new_face1.outer_half_edge = half_edge1
        new_face2.outer_half_edge = half_edge2
        looping_edge = half_edge2
        while True:
            looping_edge.incident_face = new_face2
            looping_edge.target.incident_edges_and_faces.append((new_face2, looping_edge))
            if looping_edge.target == v2: break
            looping_edge = looping_edge.next
            
        half_edge1.next = looping_edge.next
        half_edge1.next.prev = half_edge1
        looping_edge.next = half_edge2
        half_edge2.prev = looping_edge
        looping_edge = half_edge1
        while True:
            looping_edge.incident_face = new_face1
            looping_edge.target.incident_edges_and_faces.append((new_face1, looping_edge))
            if looping_edge.target == v1: break
            looping_edge = looping_edge.next
            
        self.faces.remove(common_face)
        for v in self.vertices:
            for temp in v.incident_edges_and_faces:
                if temp[0] == common_face:
                    v.incident_edges_and_faces.remove(temp)
                    break 
        
        self.faces.append(new_face1)
        self.faces.append(new_face2)  
             
            

    def construct_polygon(self, points):
        dcel_vertices = []
        
        for (x, y) in points:
            dcel_vertices.append(self.add_vertex(x, y))
        
        num_vertices = len(dcel_vertices)
        first_edge1 = None
        first_edge2 = None
        prev_edge1 = None
        prev_edge2 = None
        
        for i in range(num_vertices):
            v1 = dcel_vertices[i]
            v2 = dcel_vertices[(i+1)%num_vertices]
            half_edge1, half_edge2 = self.add_edge(v1, v2)
            
            if prev_edge1:
                prev_edge1.next = half_edge1
                half_edge1.prev = prev_edge1
                
            if prev_edge2:
                prev_edge2.next = half_edge2
                half_edge2.prev = prev_edge2
                
            if i == 0:
                first_edge1 = half_edge1
                first_edge2 = half_edge2
            
            prev_edge1 = half_edge1
            prev_edge2 = half_edge2
            
        prev_edge1.next = first_edge1
        prev_edge2.next = first_edge2
        first_edge1.prev = prev_edge1
        first_edge2.prev = prev_edge2
        
        self.add_face(first_edge1)
        
        

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
                max_cusp_vertices.append(vertex)

            # Check conditions for max cusp vertex
            elif (prev_vertex.y > vertex.y and next_vertex.y > vertex.y and angle < 180):
                min_cusp_vertices.append(vertex)

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
            
    def print_faces(self):
        for face in self.faces:
            if face.outer_half_edge:
                half_edge = face.outer_half_edge
                print("Face:")
            # List to store the vertices of the current face
                vertices = []
            # Start traversing from the outer_half_edge of the face
                start_half_edge = half_edge
                while True:
                    
                    origin_vertex = half_edge.origin
                # Append the vertex coordinates to the list
                    vertices.append((origin_vertex.x, origin_vertex.y))
                # Move to the next half edge in the face boundary
                    half_edge = half_edge.next
                # Stop when we've looped back to the starting half edge
                    if half_edge == start_half_edge or half_edge == None:
                        break
            # Print the vertices of the face
                print(vertices)




if __name__ == "__main__":
    dcel = DCEL()
    # Use the provided points list representing a polygon
    points = [(50, 0), (100, 50), (75, 75), (100, 100), (50, 150), (0, 100), (25, 75), (0, 50)]
    # points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    dcel.construct_polygon(points)

    # Find and display the vertex types
    vertex_types = dcel.find_vertices()

    # print("\nStart Vertices:")
    # for vertex in vertex_types["start_vertices"]:
    #     print(f"({vertex.x}, {vertex.y})")
    
    # print("\nEnd Vertices:")
    # for vertex in vertex_types["end_vertices"]:
    #     print(f"({vertex.x}, {vertex.y})")
    
    # print("\nMin Cusp Vertices:")
    # for vertex in vertex_types["min_cusp_vertices"]:
    #     print(f"({vertex.x}, {vertex.y})")
    
    # print("\nMax Cusp Vertices:")
    # for vertex in vertex_types["max_cusp_vertices"]:
    #     print(f"({vertex.x}, {vertex.y})")
        
    dcel.add_diagonal(dcel.vertices[1], dcel.vertices[6])
    dcel.add_diagonal(dcel.vertices[7], dcel.vertices[1])
    print(dcel.faces)
    dcel.print_faces()
        