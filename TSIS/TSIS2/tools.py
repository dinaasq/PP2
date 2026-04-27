import pygame
from datetime import datetime

def get_timestamped_filename():
    """Создает уникальное имя файла для сохранения."""
    return f"paint_save_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

def flood_fill(surface, x, y, new_color):
    """Алгоритм заливки (BFS)."""
    try:
        target_color = surface.get_at((x, y))
    except IndexError:
        return
    if target_color == new_color:
        return
    
    width, height = surface.get_size()
    queue = [(x, y)]
    visited = {(x, y)}

    while queue:
        curr_x, curr_y = queue.pop(0)
        if surface.get_at((curr_x, curr_y)) == target_color:
            surface.set_at((curr_x, curr_y), new_color)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = curr_x + dx, curr_y + dy
                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited.add((nx, ny))

# Функции отрисовки геометрических фигур
def draw_rect(surf, start, end, thick, color):
    x, y = min(start[0], end[0]), min(start[1], end[1])
    w, h = abs(start[0] - end[0]), abs(start[1] - end[1])
    pygame.draw.rect(surf, color, (x, y, w, h), thick)

def draw_circle(surf, start, end, thick, color):
    r = int(((start[0] - end[0])**2 + (start[1] - end[1])**2)**0.5)
    pygame.draw.circle(surf, color, start, r, thick)

def draw_square(surf, start, end, thick, color):
    side = max(abs(start[0] - end[0]), abs(start[1] - end[1]))
    x = start[0] if end[0] > start[0] else start[0] - side
    y = start[1] if end[1] > start[1] else start[1] - side
    pygame.draw.rect(surf, color, (x, y, side, side), thick)

def draw_right_triangle(surf, start, end, thick, color):
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(surf, color, points, thick)

def draw_equilateral_triangle(surf, start, end, thick, color):
    width = end[0] - start[0]
    points = [(start[0] + width / 2, start[1]), (start[0], end[1]), (end[0], end[1])]
    pygame.draw.polygon(surf, color, points, thick)

def draw_rhombus(surf, start, end, thick, color):
    mx, my = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
    points = [(mx, start[1]), (end[0], my), (mx, end[1]), (start[0], my)]
    pygame.draw.polygon(surf, color, points, thick)