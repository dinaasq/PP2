import pygame
import random
import os

# Game configuration (tweak these to change the difficulty / look)

WIDTH, HEIGHT = 500, 700      # Window size in pixels
FPS = 60                      # Frames per second
LANE_COUNT = 3                # Number of road lanes
ROAD_LEFT = 70                # X coordinate where the road starts
ROAD_RIGHT = WIDTH - 70       # X coordinate where the road ends
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANE_WIDTH = ROAD_WIDTH // LANE_COUNT

# Speed-up rule: every N coins increases enemy speed by SPEED_STEP
COINS_FOR_SPEEDUP = 5
SPEED_STEP = 1

# Coin specification: (color, weight/points, spawn probability)
COIN_TYPES = [
    {"name": "bronze", "color": (205, 127, 50),  "weight": 1, "prob": 0.60},
    {"name": "silver", "color": (192, 192, 192), "weight": 2, "prob": 0.30},
    {"name": "gold",   "color": (255, 215,   0), "weight": 3, "prob": 0.10},
]



# Helpers

def lane_to_x(lane_index: int, obj_width: int) -> int:
    """Return the X coordinate that horizontally centers an object in a lane."""
    lane_center = ROAD_LEFT + LANE_WIDTH * lane_index + LANE_WIDTH // 2
    return lane_center - obj_width // 2


def random_coin_type() -> dict:
    """Pick a coin type respecting the configured spawn probabilities."""
    r = random.random()
    cumulative = 0.0
    for coin in COIN_TYPES:
        cumulative += coin["prob"]
        if r <= cumulative:
            return coin
    return COIN_TYPES[0]



# Sprite classes
class Player(pygame.sprite.Sprite):
    

    def __init__(self, image: pygame.Surface):
        super().__init__()
        # Use the loaded car.png picture instead of a colored rectangle
        self.image = image
        self.rect = self.image.get_rect()
        self.lane = 1  # Start in middle lane
        self.rect.x = lane_to_x(self.lane, self.rect.width)
        self.rect.y = HEIGHT - self.rect.height - 20

    def move(self, direction: int) -> None:
        
        new_lane = self.lane + direction
        if 0 <= new_lane < LANE_COUNT:
            self.lane = new_lane
            self.rect.x = lane_to_x(self.lane, self.rect.width)


class Enemy(pygame.sprite.Sprite):
    

    def __init__(self, speed: int, image: pygame.Surface):
        super().__init__()
        # Use the loaded enemy.png picture instead of a colored rectangle
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = lane_to_x(random.randint(0, LANE_COUNT - 1), self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = speed

    def update(self):
        # Move downward each frame; remove sprite once off-screen
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    

    def __init__(self, speed: int):
        super().__init__()
        coin_type = random_coin_type()
        self.weight = coin_type["weight"]
        self.color = coin_type["color"]
        self.name = coin_type["name"]

        # Bigger coins (more points) are visually larger
        size = 18 + self.weight * 4
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (size // 2, size // 2), size // 2)
        pygame.draw.circle(self.image, (0, 0, 0), (size // 2, size // 2), size // 2, 2)

        self.rect = self.image.get_rect()
        self.rect.x = lane_to_x(random.randint(0, LANE_COUNT - 1), self.rect.width)
        self.rect.y = -50
        self.speed = speed

    def update(self):
        # Coins scroll down with the road
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 22, bold=True)

    
    # car.png    -> player car
    # enemy.png  -> opposing cars
    # Both files are expected to live next to this script.
    base_dir = os.path.dirname(os.path.abspath(__file__))
    car_size = (LANE_WIDTH - 60, 90)
    player_image = pygame.image.load(os.path.join(base_dir, "car.png")).convert_alpha()
    player_image = pygame.transform.smoothscale(player_image, car_size)

    enemy_image = pygame.image.load(os.path.join(base_dir, "enemy.png")).convert_alpha()
    enemy_image = pygame.transform.smoothscale(enemy_image, car_size)

    
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()

    
    player = Player(player_image)
    all_sprites.add(player)

    
    score = 0                # Coin points collected
    coins_collected = 0      # Total number of coins (used for speed-up trigger)
    enemy_speed = 5          # Current enemy / world speed (also used for coins)
    last_speedup_threshold = 0  # Tracks the last threshold we already triggered

    # Spawn timers (in milliseconds)
    SPAWN_ENEMY = pygame.USEREVENT + 1
    SPAWN_COIN = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_ENEMY, 1200)
    pygame.time.set_timer(SPAWN_COIN, 700)

    running = True
    game_over = False

    while running:
        # ---- Event handling ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    player.move(-1)
                elif event.key == pygame.K_RIGHT:
                    player.move(+1)
            elif event.type == SPAWN_ENEMY and not game_over:
                # Spawn an enemy car at the current world speed
                e = Enemy(enemy_speed, enemy_image)
                enemies.add(e)
                all_sprites.add(e)
            elif event.type == SPAWN_COIN and not game_over:
                # Spawn a coin (weighted by COIN_TYPES probabilities)
                c = Coin(enemy_speed)
                coins.add(c)
                all_sprites.add(c)

        if not game_over:
            # ---- Updates ----
            all_sprites.update()

            # Coin pickup: add the coin's weight to the score
            picked = pygame.sprite.spritecollide(player, coins, dokill=True)
            for coin in picked:
                score += coin.weight
                coins_collected += 1

            # Enemy collision = game over
            if pygame.sprite.spritecollide(player, enemies, dokill=False):
                game_over = True

            # ---- Speed-up rule ----
            # Every COINS_FOR_SPEEDUP coins, bump the enemy speed by SPEED_STEP.
            # Using thresholds prevents repeated speed-ups on the same coin count.
            new_threshold = coins_collected // COINS_FOR_SPEEDUP
            if new_threshold > last_speedup_threshold:
                enemy_speed += SPEED_STEP
                last_speedup_threshold = new_threshold

        # ---- Drawing ----
        screen.fill((50, 50, 50))  # Background (grass)

        # Road
        pygame.draw.rect(screen, (20, 20, 20),
                         (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))
        # Lane dividers (dashed)
        for i in range(1, LANE_COUNT):
            x = ROAD_LEFT + LANE_WIDTH * i
            for y in range(0, HEIGHT, 40):
                pygame.draw.rect(screen, (255, 255, 255), (x - 2, y, 4, 20))

        all_sprites.draw(screen)

        # HUD
        hud = font.render(
            f"Score: {score}   Coins: {coins_collected}   Enemy speed: {enemy_speed}",
            True, (255, 255, 255),
        )
        screen.blit(hud, (10, 10))

        if game_over:
            msg = font.render("GAME OVER - close window to exit", True, (255, 80, 80))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()