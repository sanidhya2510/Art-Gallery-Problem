import time

class TrapezoidalisationApp:
    def __init__(self, canvas, dcel):
        self.canvas = canvas
        self.dcel = dcel
        self.canvas_width = 500
        self.canvas_height = 500
        self.padding = 50  # Padding for the axes and graph
        self.origin_x = self.padding
        self.origin_y = self.canvas_height - self.padding
        self.horizontal_lines = []  # Store the IDs of horizontal lines

    def draw_trapezoidalisation(self):
        vertices = sorted(self.dcel.vertices, key=lambda v: v.y, reverse=True)  # Sort vertices top to bottom

        for vertex in vertices:
            self.draw_horizontal_line(vertex)
            self.canvas.update()
            # time.sleep(0.4)  # Delay between each line for visualization
            # self.remove_horizontal_line(vertex)  # Remove the line after it's drawn

    def draw_horizontal_line(self, vertex):
        x1 = 0  # Horizontal line from x=0 to width
        x2 = self.canvas_width - 2 * self.padding

        # Adjust for canvas coordinates (since Tkinter canvas has inverted y-axis)
        adjusted_y = self.origin_y - vertex.y
        line_id = self.canvas.create_line(self.origin_x + x1, adjusted_y, self.origin_x + x2, adjusted_y, fill="blue", dash=(4, 2))
        self.horizontal_lines.append(line_id)

    def remove_horizontal_line(self, vertex):
        """Remove the horizontal line corresponding to a vertex."""
        if self.horizontal_lines:
            line_id = self.horizontal_lines.pop(0)  # Remove the first line added (for the vertex being processed)
            self.canvas.delete(line_id)

    def reset_canvas(self):
        """Clear all horizontal lines and reset the drawing area."""
        for line_id in self.horizontal_lines:
            self.canvas.delete(line_id)
        self.horizontal_lines.clear()
