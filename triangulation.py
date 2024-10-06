import time

class TriangulationApp:
    def __init__(self, canvas, dcel, monotone_app):
        self.canvas = canvas
        self.dcel = dcel
        self.monotone_app = monotone_app
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50 
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding

    def triangulate_polygon(self):
        pending_diagonals = []
        face_count = 1
        for face in self.dcel.faces:
            print(f"Face {face_count}:")
            face_count+=1
            looping_edge = face.outer_half_edge
            starting_vertex = looping_edge.origin
            vertex_list = []

            while True:
                vertex_list.append(looping_edge.origin)
                looping_edge = looping_edge.next
                if looping_edge.origin == starting_vertex:
                    break
                
            sorted_vertices = sorted(vertex_list, key=lambda v: (-v.y, v.x))
            top_vertex = sorted_vertices[0]
            bottom_vertex = sorted_vertices[-1]

            chain1 = []
            chain2 = []
            
            while vertex_list[0] != top_vertex:
                temp_vertex = vertex_list[0]
                vertex_list.remove(temp_vertex)
                vertex_list.append(temp_vertex)
            
            switching = False
            chain2.append(top_vertex)
            for k in vertex_list:
                if not switching: chain1.append(k)
                else: chain2.append(k)
                if k == bottom_vertex:
                    switching = True
            chain2.append(bottom_vertex)
            
            chain1 = sorted(chain1, key=lambda v: (-v.y, v.x))
            chain2 = sorted(chain2, key=lambda v: (-v.y, v.x))
            
            Q = []
            Q.append(sorted_vertices[0])
            sorted_vertices.pop(0)
            Q.append(sorted_vertices[0])
            sorted_vertices.pop(0)
            
            left_chain = []
            right_chain = []
            
            
            slope1 = (chain1[1].y-top_vertex.y)/(chain1[1].x-top_vertex.x)
            slope2 = (chain2[1].y-top_vertex.y)/(chain2[1].x-top_vertex.x)
            
            
            
            if slope1 > 0 and slope2 < 0:
                left_chain = chain1
                right_chain = chain2
            
            elif slope2 > 0 and slope1 < 0:
                left_chain = chain2
                right_chain = chain1
            
            else:
                if slope1 > slope2:
                    right_chain = chain1
                    left_chain = chain2
                else: 
                    right_chain = chain2
                    left_chain = chain1
            
            print("Left Chain:")
            for vertex in left_chain:
                print(f"Vertex({vertex.x}, {vertex.y})")

            print("Right Chain:")
            for vertex in right_chain:
                print(f"Vertex({vertex.x}, {vertex.y})")
                
            # sorted_vertices.pop()
            for k in sorted_vertices:
                if k in left_chain and Q[-1] in left_chain:
                    Q.append(k)
                    while True and len(Q) >=3:
                        v1, v2, v3 = Q[-1], Q[-2], Q[-3]
                        if ((v3.y-v1.y)/(v3.x-v1.x)>0 and v2.y-v1.y-((v3.y-v1.y)/(v3.x-v1.x))*(v2.x-v1.x) <= 0) or ((v3.y-v1.y)/(v3.x-v1.x)<0 and v2.y-v1.y-((v3.y-v1.y)/(v3.x-v1.x))*(v2.x-v1.x) >= 0):
                            break
                        else:
                            self.monotone_app.draw_diagonal_only(v1, v3)
                            pending_diagonals.append((v1, v3))
                            u = Q.pop()
                            Q.pop()
                            Q.append(u)
                elif k in right_chain and Q[-1] in right_chain:
                    Q.append(k)
                    while True and len(Q)>=3:
                        v1, v2, v3 = Q[-1], Q[-2], Q[-3]
                        if ((v3.y-v1.y)/(v3.x-v1.x)<0 and v2.y-v1.y-((v3.y-v1.y)/(v3.x-v1.x))*(v2.x-v1.x) <= 0) or ((v3.y-v1.y)/(v3.x-v1.x)>0 and v2.y-v1.y-((v3.y-v1.y)/(v3.x-v1.x))*(v2.x-v1.x) >= 0):
                            break
                        else:
                            self.monotone_app.draw_diagonal_only(v1, v3)
                            pending_diagonals.append((v1, v3))
                            u = Q.pop()
                            Q.pop()
                            Q.append(u)
                else:
                    Q.pop(0)
                    while len(Q) >= 2:
                        self.monotone_app.draw_diagonal_only(Q[0], k)
                        pending_diagonals.append((Q[0], k))
                        Q.pop(0)
                    self.monotone_app.draw_diagonal_only(Q[0], k)
                    pending_diagonals.append((Q[0], k))
                    Q.append(k)
        
        for (v1, v2) in pending_diagonals:
            self.dcel.add_diagonal(v1, v2)          
            
                        
                    
                        
                    
            
            
            
              

                
            