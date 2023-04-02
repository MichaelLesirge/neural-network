import pygame

def to_size_relitive_value(size: int, value: float, reverse = False) -> int:
    relitive_point = int(size * value)
    if reverse: relitive_point = size - relitive_point
    return relitive_point

def to_rect_relitive_points(rect: pygame.rect.Rect, point: tuple[float, float], reverse_x = False, reverse_y = False) -> tuple[int, int]:
    return to_size_relitive_value(rect.width, point[0], reverse_x), to_size_relitive_value(rect.height, point[1], reverse_y)

def rect_centered_point(rect: pygame.rect.Rect, point: tuple[int, int]) -> tuple[int, int]:
    return point[0] - (rect.width // 2), point[1] - (rect.height // 2)
