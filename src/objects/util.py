import math

import pygame

from src.constant import FONT_PATH


def calculate_distance_line(a, b):
    (x1, y1) = a
    (x2, y2) = b
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def calculate_distance_dot(a, b):
    dist = math.sqrt((a - b) ** 2)
    return dist


def get_width_by_height(height, image):
    origin_width = image.get_width()
    origin_height = image.get_height()
    return (origin_width / origin_height) * height


def get_height_by_width(width, image):
    origin_width = image.get_width()
    origin_height = image.get_height()
    return (origin_height / origin_width) * width


def get_font(size):
    return pygame.font.Font(FONT_PATH, size)
