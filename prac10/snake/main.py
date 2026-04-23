import pygame
import random

pygame.init()

# screen
WIDTH, HEIGHT = 600, 400
BLOCK = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Snake")

clock = pygame.time.Clock()

# colors
BG = (10, 10, 20)
GRID = (25, 25, 40)
SNAKE_HEAD = (0, 255, 200)
SNAKE_BODY = (0, 180, 255)
FOOD = (255, 60, 120)
TEXT = (220, 220, 255)

# snake
snake = [(100, 100), (80, 100), (60, 100)]
direction = (BLOCK, 0)

# -food
def spawn_food():
    while True:
        x = random.randint(0, (WIDTH - BLOCK) // BLOCK) * BLOCK
        y = random.randint(0, (HEIGHT - BLOCK) // BLOCK) * BLOCK
        if (x, y) not in snake:
            return (x, y)

food = spawn_food()

# score
score = 0
level = 1
speed = 8

font = pygame.font.SysFont("arial", 22, bold=True)

# grid draw
def draw_grid():
    for x in range(0, WIDTH, BLOCK):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y))

# game loop
running = True

while running:
    clock.tick(speed)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, BLOCK):
                direction = (0, -BLOCK)
            if event.key == pygame.K_DOWN and direction != (0, -BLOCK):
                direction = (0, BLOCK)
            if event.key == pygame.K_LEFT and direction != (BLOCK, 0):
                direction = (-BLOCK, 0)
            if event.key == pygame.K_RIGHT and direction != (-BLOCK, 0):
                direction = (BLOCK, 0)

    # move
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    snake.insert(0, new_head)

    # food
    if snake[0] == food:
        score += 1
        food = spawn_food()
    else:
        snake.pop()

    # wall
    if (new_head[0] < 0 or new_head[0] >= WIDTH or
        new_head[1] < 0 or new_head[1] >= HEIGHT):
        running = False

    # level system
    level = score // 3 + 1
    speed = 8 + level * 2

    # draw
    screen.fill(BG)
    draw_grid()

    # food (glow effect)
    pygame.draw.rect(screen, FOOD, (*food, BLOCK, BLOCK), border_radius=6)

    # snake (head + body style)
    for i, block in enumerate(snake):
        color = SNAKE_HEAD if i == 0 else SNAKE_BODY
        pygame.draw.rect(screen, color, (*block, BLOCK, BLOCK), border_radius=6)

    # ---------------- HUD ----------------
    hud = font.render(f"Score: {score}   Level: {level}", True, TEXT)
    screen.blit(hud, (10, 10))

    pygame.display.update()

pygame.quit()