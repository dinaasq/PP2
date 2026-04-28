import pygame
import random
import os

# Configuration
CELL = 20                              
COLS, ROWS = 25, 25                    
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL + 40  
FPS = 10                               


FOOD_TYPES = [
    {"name": "apple",  "image_file": "apple.png",  "weight": 1, "prob": 0.60, "life_ms": 10_000},
    {"name": "banana", "image_file": "banana.png", "weight": 2, "prob": 0.30, "life_ms":  6_000},
    {"name": "cherry", "image_file": "cherry.png", "weight": 3, "prob": 0.10, "life_ms":  3_500},
]

# Cache of loaded/scaled food pictures keyed by food name.
FOOD_IMAGES: dict[str, pygame.Surface] = {}


def load_food_images() -> None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for f in FOOD_TYPES:
        path = os.path.join(base_dir, f["image_file"])
        img = pygame.image.load(path).convert_alpha()
        # Scale to (almost) one cell so the picture fits the grid
        img = pygame.transform.smoothscale(img, (CELL - 2, CELL - 2))
        FOOD_IMAGES[f["name"]] = img


def random_food_type() -> dict:
    
    r = random.random()
    cumulative = 0.0
    for f in FOOD_TYPES:
        cumulative += f["prob"]
        if r <= cumulative:
            return f
    return FOOD_TYPES[0]


# Food class
class Food:

    def __init__(self, occupied_cells: set):
        f = random_food_type()
        self.name = f["name"]
        self.image = FOOD_IMAGES[self.name]   # cached picture for this food
        self.weight = f["weight"]
        self.life_ms = f["life_ms"]
        self.spawn_time = pygame.time.get_ticks()
        # Pick a random empty cell (avoid spawning on the snake)
        free_cells = [
            (x, y)
            for x in range(COLS)
            for y in range(ROWS)
            if (x, y) not in occupied_cells
        ]
        self.pos = random.choice(free_cells) if free_cells else (0, 0)

    def is_expired(self) -> bool:
        return pygame.time.get_ticks() - self.spawn_time >= self.life_ms

    def time_left_ratio(self) -> float:
        elapsed = pygame.time.get_ticks() - self.spawn_time
        return max(0.0, 1.0 - elapsed / self.life_ms)

    def draw(self, surf: pygame.Surface):
        
        x = self.pos[0] * CELL + 1
        y = self.pos[1] * CELL + 41    
        surf.blit(self.image, (x, y))
       



# Game
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 20, bold=True)

    # Load apple.png / banana.png / cherry.png from this script's folder.
    load_food_images()

    # Snake state: list of (x, y) cells. Head is the LAST element.
    snake = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)               # Initially moving right
    pending_growth = 0               # Cells to grow next ticks (set when eating)

    # Food state: a list to allow several foods on the board at once
    foods: list[Food] = []
    SPAWN_FOOD = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_FOOD, 1500)  # Try to spawn a new food every 1.5s

    score = 0
    game_over = False

    def occupied_cells() -> set:
        return set(snake)

    foods.append(Food(occupied_cells()))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)
            elif event.type == SPAWN_FOOD and not game_over:
                if len(foods) < 4:
                    foods.append(Food(occupied_cells()))

        if not game_over:
            head_x, head_y = snake[-1]
            new_head = (head_x + direction[0], head_y + direction[1])

            if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
                game_over = True
            elif new_head in snake:
                game_over = True
            else:
                snake.append(new_head)

                eaten_index = None
                for i, food in enumerate(foods):
                    if food.pos == new_head:
                        eaten_index = i
                        break
                if eaten_index is not None:
                    food = foods.pop(eaten_index)
                    score += food.weight
                    pending_growth += food.weight
                    foods.append(Food(occupied_cells()))

                if pending_growth > 0:
                    pending_growth -= 1
                else:
                    snake.pop(0)

            foods = [f for f in foods if not f.is_expired()]
            if not foods:
                foods.append(Food(occupied_cells()))

        # ---- Draw ----
        screen.fill((20, 20, 20))
        pygame.draw.rect(screen, (40, 40, 40), (0, 0, WIDTH, 40))
        hud = font.render(
            f"Score: {score}   Length: {len(snake)}   Foods on board: {len(foods)}",
            True, (255, 255, 255),
        )
        screen.blit(hud, (10, 10))

        pygame.draw.rect(screen, (10, 50, 10), (0, 40, WIDTH, HEIGHT - 40))

        for i, (x, y) in enumerate(snake):
            color = (50, 220, 50) if i == len(snake) - 1 else (40, 180, 40)
            pygame.draw.rect(
                screen, color,
                (x * CELL + 1, y * CELL + 41, CELL - 2, CELL - 2),
            )

        for food in foods:
            food.draw(screen)

        if game_over:
            msg = font.render("GAME OVER - close window to exit", True, (255, 80, 80))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()