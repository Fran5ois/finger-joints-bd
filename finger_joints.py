from build123d import Rectangle, Location, Align
import math

def generate_finger_joints(edges, material_thickness, finger_length):
    """
    Generate rectangles (finger joints) along given edges.
    Args:
        edges: A single edge or a list of edges (build123d Edge objects)
        material_thickness: The width of each finger (rectangle) (float)
        finger_length: The length/depth of each finger (float)
    Returns:
        List of lists of Rectangle objects (one list per edge)
    """
    # Accept both single edge or list
    if not isinstance(edges, (list, tuple)):
        edges = [edges]
    all_fingers = []
    for edge in edges:
        edge_length = edge.length
        # Compute how many fingers fit (ensure odd/even symmetry)
        n_fingers = max(1, int((edge_length + finger_length) // (finger_length * 2)))
        total_finger_span = (n_fingers * 2 - 1) * finger_length
        # Center the fingers on the edge
        start_offset = (edge_length - total_finger_span) / 2
        # Get edge direction and start point
        start = edge.start_point()
        end = edge.end_point()
        dx = end.X - start.X
        dy = end.Y - start.Y
        angle = math.atan2(dy, dx)
        # Place rectangles
        fingers = []
        for i in range(n_fingers * 2 - 1):
            if i % 2 == 0:  # Only place on even slots
                offset = start_offset + i * finger_length
                cx = start.X + math.cos(angle) * (offset + finger_length / 2)
                cy = start.Y + math.sin(angle) * (offset + finger_length / 2)
                loc = Location((cx, cy, 0), (0, 0, math.degrees(angle)))
                rect = Rectangle(finger_length, material_thickness,align=(Align.CENTER, Align.CENTER))
                fingers.append(rect.locate(loc))
        all_fingers.append(fingers)
    return all_fingers
