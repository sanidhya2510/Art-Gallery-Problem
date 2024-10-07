import tkinter as tk

class DualGraphApp:
    def __init__(self, canvas, dcel, triangulation_app):
        self.canvas = canvas
        self.dcel = dcel
        self.triangulation_app = triangulation_app
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding
        self.axis_length = self.canvas_width - 2 * self.padding  # Length of positive axes
    
    def transform_coordinates(self, x, y):
        """Transforms (x, y) to fit canvas and invert y-axis."""
        transformed_x = self.origin_x + x
        transformed_y = self.origin_y - y  # Invert y-axis
        return transformed_x, transformed_y

    def create_dual_graph(self):
        # Create a dictionary to store the centroids of each face
        centroids = {}

        print(f"Number of faces: {len(self.dcel.faces)}")
        
        # Loop through each face in the DCEL to calculate its centroid
        for face in self.dcel.faces:
            if face.outer_half_edge:
                vertices = []
                half_edge = face.outer_half_edge
                start_edge = half_edge
                
                # Collect the vertices of the face (triangle)
                while True:
                    origin = half_edge.origin
                    vertices.append((origin.x, origin.y))
                    half_edge = half_edge.next
                    if half_edge == start_edge:
                        break

                # Calculate the centroid of the face (triangle)
                centroid_x = sum(v[0] for v in vertices) / 3.0
                centroid_y = sum(v[1] for v in vertices) / 3.0
                centroids[face] = (centroid_x, centroid_y)
                
                print("Triangle vertices:")
                for v in vertices:
                    print(f"({v[0]}, {v[1]})")

                # Transform centroid coordinates to canvas space
                transformed_centroid_x, transformed_centroid_y = self.transform_coordinates(centroid_x, centroid_y)

                # Draw the centroid as a small circle on the canvas
                self.draw_point(transformed_centroid_x, transformed_centroid_y)

        # Now we will connect centroids of adjacent triangles
        for face in self.dcel.faces:
            if face.outer_half_edge:
                half_edge = face.outer_half_edge
                start_edge = half_edge
                # Loop through the edges of the face
                while True:
                    twin_edge = half_edge.twin
                    if twin_edge and twin_edge.incident_face in centroids:
                        # Draw a line connecting the centroids of adjacent triangles
                        centroid1 = centroids[face]
                        centroid2 = centroids[twin_edge.incident_face]
                        
                        # Transform the centroids to canvas coordinates
                        transformed_centroid1 = self.transform_coordinates(centroid1[0], centroid1[1])
                        transformed_centroid2 = self.transform_coordinates(centroid2[0], centroid2[1])
                        
                        self.draw_line(transformed_centroid1, transformed_centroid2)

                    half_edge = half_edge.next
                    if half_edge == start_edge:
                        break

    def draw_point(self, x, y, radius=3, color="black"):
        """Draw a small circle at the given (x, y) position."""
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

    def draw_line(self, point1, point2, color="black"):
        """Draw a solid black line between two points on the canvas."""
        self.canvas.create_line(point1[0], point1[1], point2[0], point2[1], fill=color)
