import random
import time
import math
import tkinter as tk
from tkinter import simpledialog
from dcel import DCEL  # Import the DCEL class

class GeneratePolygonApp:
    def __init__(self, canvas):
        self.canvas = canvas
        self.points = []
        self.num_vertices = 0
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50  # Padding for the axes and graph
        self.axis_length = self.canvas_width - 2 * self.padding  # Length of positive axes
        self.dcel = DCEL()  # Create an instance of the DCEL

    def generate_polygon(self):
        # Ask the user for the number of vertices
        self.num_vertices = simpledialog.askinteger("Input", "Enter number of vertices (n):", minvalue=3, maxvalue=20)
        if self.num_vertices:
            self.canvas.delete("all")  # Clear canvas for new polygon
            self.draw_axes()  # Draw positive coordinate axes
            self.points = self.generate_random_points(self.num_vertices)
            centroid = self.calculate_centroid(self.points)
            sorted_points = self.sort_points_anticlockwise(self.points, centroid)
            
            # Store the generated polygon in the DCEL
            self.dcel.construct_polygon(sorted_points)
            # Draw the polygon with delay
            self.draw_polygon_with_delay(sorted_points)

    def draw_axes(self):
        # Draw positive X and Y axes
        origin_x = self.padding
        origin_y = self.canvas_height - self.padding

        # Draw the positive X-axis (rightwards line)
        self.canvas.create_line(origin_x, origin_y, origin_x + self.axis_length, origin_y, fill="black", arrow=tk.LAST)
        
        # Draw the positive Y-axis (upwards line)
        self.canvas.create_line(origin_x, origin_y, origin_x, origin_y - self.axis_length, fill="black", arrow=tk.LAST)

        # Add labels to the axes
        self.canvas.create_text(origin_x + self.axis_length + 10, origin_y + 10, text="X", fill="black", font=("Arial", 10))
        self.canvas.create_text(origin_x - 10, origin_y - self.axis_length - 10, text="Y", fill="black", font=("Arial", 10))

    def generate_random_points(self, n):
        # Generate n random points within the first quadrant (positive X and Y axes)
        points = [(random.randint(0, self.axis_length),
                   random.randint(0, self.axis_length)) for _ in range(n)]
        return points

    def calculate_centroid(self, points):
        # Calculate the centroid of a set of points
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        centroid_x = sum(x_coords) / len(points)
        centroid_y = sum(y_coords) / len(points)
        return (centroid_x, centroid_y)

    def sort_points_anticlockwise(self, points, centroid):
        # Sort points in an anti-clockwise direction relative to the centroid
        def angle_from_centroid(point):
            return math.atan2(point[1] - centroid[1], point[0] - centroid[0])

        return sorted(points, key=angle_from_centroid)

    def draw_polygon_with_delay(self, points):
        # Draw each point and line with a delay of 0.4 seconds
        origin_x = self.padding
        origin_y = self.canvas_height - self.padding

        for i in range(len(points)):
            x, y = points[i]
            # Adjust coordinates to fit within the positive axes
            adjusted_x = origin_x + x
            adjusted_y = origin_y - y

            # Draw the point
            self.canvas.create_oval(adjusted_x-3, adjusted_y-3, adjusted_x+3, adjusted_y+3, fill="black")
            
            # Display coordinates next to the point with a smaller font size
            self.canvas.create_text(adjusted_x + 10, adjusted_y - 10, text=f"({x}, {y})", fill="blue", font=("Arial", 8))

            # Update the canvas to show the point and its coordinates
            self.canvas.update()
            # time.sleep(0.4)

            # Draw the line connecting the current point to the next one
            next_point = points[(i + 1) % len(points)]  # Wrap around to first point
            adjusted_next_x = origin_x + next_point[0]
            adjusted_next_y = origin_y - next_point[1]
            self.canvas.create_line(adjusted_x, adjusted_y, adjusted_next_x, adjusted_next_y, fill="blue")
            
            # Update the canvas to show the connecting line
            self.canvas.update()
            time.sleep(0.4)

# Example usage within the main application will be handled as before.
