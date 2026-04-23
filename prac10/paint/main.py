import pygame
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)

screen.fill(WHITE)

# состояние
running = True
drawing = False
mode = "pen"  # pen, rect, circle, eraser
color = BLACK
radius = 5

start_pos = None
points = []

# ---------------- DRAW SMOOTH LINE ----------------
def draw_line(screen, start, end, color, width):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    steps = max(abs(dx), abs(dy))

    for i in range(steps):
        t = i / steps
        x = int(start[0] * (1 - t) + end[0] * t)
        y = int(start[1] * (1 - t) + end[1] * t)
        pygame.draw.circle(screen, color, (x, y), width)

# ---------------- MAIN LOOP ----------------
while running:

    pressed = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # клавиши режимов
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                mode = "pen"
            if event.key == pygame.K_2:
                mode = "rect"
            if event.key == pygame.K_3:
                mode = "circle"
            if event.key == pygame.K_4:
                mode = "eraser"

            # цвета
            if event.key == pygame.K_r:
                color = RED
            if event.key == pygame.K_g:
                color = GREEN
            if event.key == pygame.K_b:
                color = BLUE
            if event.key == pygame.K_k:
                color = BLACK

            # очистка экрана
            if event.key == pygame.K_c:
                screen.fill(WHITE)

        # начало рисования
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos
            points = [event.pos]

        # конец рисования
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            # RECTANGLE
            if mode == "rect":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                w = abs(start_pos[0] - end_pos[0])
                h = abs(start_pos[1] - end_pos[1])
                pygame.draw.rect(screen, color, (x, y, w, h), 2)

            # CIRCLE
            if mode == "circle":
                radius_circle = int(math.dist(start_pos, end_pos))
                pygame.draw.circle(screen, color, start_pos, radius_circle, 2)

    # ---------------- PEN / ERASER ----------------
    if drawing:
        mouse = pygame.mouse.get_pos()

        if mode == "pen":
            points.append(mouse)

            if len(points) > 1:
                draw_line(screen, points[-2], points[-1], color, radius)

        if mode == "eraser":
            points.append(mouse)

            if len(points) > 1:
                draw_line(screen, points[-2], points[-1], WHITE, radius * 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()