import math


def calculate_distance_line(a, b):
    (x1, y1) = a
    (x2, y2) = b
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def calculate_distance_dot(a, b):
    dist = math.sqrt((a - b) ** 2)
    return dist
