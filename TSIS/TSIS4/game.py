"""Snake game core: snake, foods, poison, power-ups, obstacles, levels."""
import random
import pygame

from config import (
    CELL, COLS, ROWS, HUD_HEIGHT, WIDTH, HEIGHT,
    BLACK, WHITE, GRID, WALL, RED, DARK_RED, GOLD, SILVER, GREEN,
    BLUE, CYAN, PURPLE, ORANGE, HUD_BG,
    START_LENGTH, BASE_SPEED, SPEED_PER_LEVEL, FOOD_PER_LEVEL,
    POWERUP_FIELD_TTL_MS, POWERUP_EFFECT_MS,
    SPEED_BOOST_MULT, SLOW_MOTION_MULT,
    FOOD_TTL_MS, POISON_TTL_MS,
    OBSTACLES_FROM_LEVEL, OBSTACLES_PER_LEVEL, OBSTACLE_MAX,
)


def cell_rect(cx, cy):
    return pygame.Rect(cx * CELL, HUD_HEIGHT + cy * CELL, CELL, CELL)


class Food:
    """Weighted, time-limited food (Practice 11 base)."""
    def __init__(self, pos, value, color, born_ms):
        self.pos = pos
        self.value = value
        self.color = color
        self.born_ms = born_ms

    def expired(self, now_ms):
        return now_ms - self.born_ms > FOOD_TTL_MS

    def draw(self, surf):
        r = cell_rect(*self.pos).inflate(-4, -4)
        pygame.draw.rect(surf, self.color, r, border_radius=6)
        pygame.draw.rect(surf, WHITE, r, 1, border_radius=6)


class Poison:
    """Poison food: shrinks the snake by 2."""
    def __init__(self, pos, born_ms):
        self.pos = pos
        self.born_ms = born_ms

    def expired(self, now_ms):
        return now_ms - self.born_ms > POISON_TTL_MS

    def draw(self, surf):
        r = cell_rect(*self.pos).inflate(-4, -4)
        pygame.draw.rect(surf, DARK_RED, r, border_radius=6)
        # Skull-ish dots
        pygame.draw.circle(surf, WHITE, (r.centerx - 4, r.centery - 2), 2)
        pygame.draw.circle(surf, WHITE, (r.centerx + 4, r.centery - 2), 2)
        pygame.draw.line(surf, WHITE,
                         (r.centerx - 4, r.centery + 4),
                         (r.centerx + 4, r.centery + 4), 2)


class PowerUp:
    """Field power-up: speed / slow / shield."""
    KINDS = ("speed", "slow", "shield")
    COLORS = {"speed": CYAN, "slow": BLUE, "shield": GOLD}

    def __init__(self, pos, kind, born_ms):
        self.pos = pos
        self.kind = kind
        self.born_ms = born_ms

    def expired(self, now_ms):
        return now_ms - self.born_ms > POWERUP_FIELD_TTL_MS

    def draw(self, surf):
        r = cell_rect(*self.pos).inflate(-3, -3)
        pygame.draw.rect(surf, self.COLORS[self.kind], r, border_radius=6)
        pygame.draw.rect(surf, WHITE, r, 2, border_radius=6)
        f = pygame.font.SysFont("arial", 14, bold=True)
        ch = {"speed": "S", "slow": "L", "shield": "*"}[self.kind]
        text = f.render(ch, True, BLACK)
        tw, th = text.get_size()
        surf.blit(text, (r.centerx - tw // 2, r.centery - th // 2))


class Snake:
    def __init__(self, color):
        cx, cy = COLS // 2, ROWS // 2
        self.body = [(cx - i, cy) for i in range(START_LENGTH)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.color = tuple(color)
        self.grow_pending = 0

    def head(self):
        return self.body[0]

    def set_color(self, color):
        self.color = tuple(color)

    def turn(self, d):
        # Disallow direct reverse
        if (d[0] == -self.direction[0] and d[1] == -self.direction[1]
                and len(self.body) > 1):
            return
        self.next_direction = d

    def step(self):
        self.direction = self.next_direction
        hx, hy = self.body[0]
        new_head = (hx + self.direction[0], hy + self.direction[1])
        self.body.insert(0, new_head)
        if self.grow_pending > 0:
            self.grow_pending -= 1
        else:
            self.body.pop()

    def grow(self, n=1):
        self.grow_pending += n

    def shrink(self, n=2):
        for _ in range(n):
            if len(self.body) > 1:
                self.body.pop()

    def hits_self(self):
        return self.body[0] in self.body[1:]

    def occupies(self):
        return set(self.body)

    def draw(self, surf, shielded=False):
        for i, (x, y) in enumerate(self.body):
            r = cell_rect(x, y).inflate(-2, -2)
            shade = max(60, 230 - i * 6)
            col = (
                min(255, self.color[0] * shade // 230),
                min(255, self.color[1] * shade // 230),
                min(255, self.color[2] * shade // 230),
            )
            pygame.draw.rect(surf, col, r, border_radius=6)
        # Head detail
        hx, hy = self.body[0]
        head_r = cell_rect(hx, hy)
        pygame.draw.circle(surf, BLACK,
                           (head_r.centerx - 4, head_r.centery - 4), 3)
        pygame.draw.circle(surf, BLACK,
                           (head_r.centerx + 4, head_r.centery - 4), 3)
        if shielded:
            pygame.draw.rect(surf, GOLD, head_r.inflate(2, 2), 2,
                             border_radius=6)


class Game:
    def __init__(self, settings, username, personal_best=0):
        self.settings = settings
        self.username = username or "PLAYER"
        self.personal_best = int(personal_best)

        self.snake = Snake(settings["snake_color"])
        self.foods = []
        self.poison = None
        self.powerup = None

        self.obstacles = set()
        self.level = 1
        self.score = 0
        self.foods_eaten = 0  # only counts NORMAL foods toward levels

        # Speed (cells per second), affected by power-ups
        self.base_speed = BASE_SPEED
        self.speed_mult = 1.0
        self.move_accum = 0.0  # seconds accumulator for stepping

        # Power-up effects
        self.active_effect = None      # ("speed"|"slow", end_ms)
        self.shield = False
        self.flash = ""
        self.flash_until = 0

        self.game_over = False
        self.death_reason = ""

        self._spawn_food(pygame.time.get_ticks(), force=True)

    # ---------- helpers ----------

    def _free_cells(self):
        used = self.snake.occupies() | self.obstacles
        used |= {f.pos for f in self.foods}
        if self.poison:
            used.add(self.poison.pos)
        if self.powerup:
            used.add(self.powerup.pos)
        return [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in used]

    def _random_free(self):
        free = self._free_cells()
        return random.choice(free) if free else None

    # ---------- spawning ----------

    def _spawn_food(self, now_ms, force=False):
        # Keep up to 2 foods on the board
        if not force and len(self.foods) >= 2:
            return
        cell = self._random_free()
        if cell is None:
            return
        # Practice 11 weighted values
        value, color = random.choices(
            [(1, RED), (3, GOLD), (5, SILVER)],
            weights=[70, 22, 8],
        )[0]
        self.foods.append(Food(cell, value, color, now_ms))

    def _spawn_poison(self, now_ms):
        if self.poison is not None:
            return
        if random.random() < 0.012:
            cell = self._random_free()
            if cell is not None:
                self.poison = Poison(cell, now_ms)

    def _spawn_powerup(self, now_ms):
        if self.powerup is not None:
            return
        if random.random() < 0.004:
            cell = self._random_free()
            if cell is None:
                return
            kind = random.choice(PowerUp.KINDS)
            self.powerup = PowerUp(cell, kind, now_ms)

    def _generate_obstacles_for_level(self):
        if self.level < OBSTACLES_FROM_LEVEL:
            return
        # Number of obstacles to place this level
        target = min(OBSTACLE_MAX,
                     OBSTACLES_PER_LEVEL * (self.level - OBSTACLES_FROM_LEVEL + 1))
        # Build a forbidden zone around the snake so we don't trap it
        head = self.snake.head()
        forbidden = set(self.snake.body)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                forbidden.add((head[0] + dx, head[1] + dy))
        # Also keep at least one cell border-free near food cells
        for f in self.foods:
            forbidden.add(f.pos)

        candidates = [(x, y) for x in range(COLS) for y in range(ROWS)
                      if (x, y) not in forbidden and (x, y) not in self.obstacles]
        random.shuffle(candidates)

        added = 0
        needed = target - len(self.obstacles)
        for cell in candidates:
            if added >= needed:
                break
            self.obstacles.add(cell)
            # Verify the snake's current head still has a free neighbor
            if not self._snake_has_breathing_room():
                self.obstacles.remove(cell)
                continue
            added += 1

    def _snake_has_breathing_room(self):
        """Make sure snake head has at least one free neighbor."""
        hx, hy = self.snake.head()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = hx + dx, hy + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS:
                if ((nx, ny) not in self.obstacles
                        and (nx, ny) not in self.snake.occupies()):
                    return True
        return False

    # ---------- gameplay ----------

    def turn(self, dx, dy):
        if not self.game_over:
            self.snake.turn((dx, dy))

    def update(self, dt):
        if self.game_over:
            return
        now_ms = pygame.time.get_ticks()

        # Expire effects
        if self.active_effect and now_ms >= self.active_effect[1]:
            self.active_effect = None
            self.speed_mult = 1.0

        # Expire field items
        self.foods = [f for f in self.foods if not f.expired(now_ms)]
        if self.poison and self.poison.expired(now_ms):
            self.poison = None
        if self.powerup and self.powerup.expired(now_ms):
            self.powerup = None

        # Random spawns
        self._spawn_food(now_ms)
        self._spawn_poison(now_ms)
        self._spawn_powerup(now_ms)

        # Step the snake at the current speed
        speed = self.base_speed * self.speed_mult
        self.move_accum += dt
        step_dt = 1.0 / speed
        while self.move_accum >= step_dt and not self.game_over:
            self.move_accum -= step_dt
            self._step_once(now_ms)

        # Flash timer
        if self.flash and now_ms > self.flash_until:
            self.flash = ""

    def _step_once(self, now_ms):
        self.snake.step()
        hx, hy = self.snake.head()

        # Wall collision
        if hx < 0 or hx >= COLS or hy < 0 or hy >= ROWS:
            if self.shield:
                self.shield = False
                self._set_flash("SHIELD ABSORBED WALL")
                # Bounce back so we don't immediately re-collide
                self.snake.body[0] = (
                    max(0, min(COLS - 1, hx)),
                    max(0, min(ROWS - 1, hy)),
                )
                return
            self._die("WALL")
            return

        # Obstacle collision
        if (hx, hy) in self.obstacles:
            if self.shield:
                self.shield = False
                self._set_flash("SHIELD ABSORBED OBSTACLE")
                # Move head off the obstacle (back one step)
                self.snake.body[0] = self.snake.body[1] if len(self.snake.body) > 1 else (hx, hy)
                return
            self._die("OBSTACLE")
            return

        # Self collision
        if self.snake.hits_self():
            if self.shield:
                self.shield = False
                self._set_flash("SHIELD ABSORBED SELF")
                self.snake.body.pop(0)  # remove the offending head
                return
            self._die("SELF")
            return

        # Food
        for f in list(self.foods):
            if f.pos == (hx, hy):
                self.foods.remove(f)
                self.snake.grow(1)
                self.score += f.value
                self.foods_eaten += 1
                if self.foods_eaten % FOOD_PER_LEVEL == 0:
                    self._level_up()
                self._spawn_food(now_ms, force=True)
                break

        # Poison
        if self.poison and self.poison.pos == (hx, hy):
            self.poison = None
            self.snake.shrink(2)
            self._set_flash("POISON -2")
            if len(self.snake.body) <= 1:
                self._die("POISON")
                return

        # Power-up
        if self.powerup and self.powerup.pos == (hx, hy):
            kind = self.powerup.kind
            self.powerup = None
            self._apply_powerup(kind, now_ms)

    def _level_up(self):
        self.level += 1
        self.base_speed = BASE_SPEED + (self.level - 1) * SPEED_PER_LEVEL
        self._set_flash(f"LEVEL {self.level}")
        self._generate_obstacles_for_level()

    def _apply_powerup(self, kind, now_ms):
        if kind == "speed":
            self.speed_mult = SPEED_BOOST_MULT
            self.active_effect = ("speed", now_ms + POWERUP_EFFECT_MS)
            self._set_flash("SPEED BOOST!")
        elif kind == "slow":
            self.speed_mult = SLOW_MOTION_MULT
            self.active_effect = ("slow", now_ms + POWERUP_EFFECT_MS)
            self._set_flash("SLOW MOTION!")
        elif kind == "shield":
            self.shield = True
            self._set_flash("SHIELD ON")

    def _set_flash(self, text, ms=900):
        self.flash = text
        self.flash_until = pygame.time.get_ticks() + ms

    def _die(self, reason):
        self.game_over = True
        self.death_reason = reason

    # ---------- draw ----------

    def draw(self, surf):
        surf.fill(BLACK)
        self._draw_grid(surf)
        # Obstacles
        for (x, y) in self.obstacles:
            r = cell_rect(x, y).inflate(-2, -2)
            pygame.draw.rect(surf, WALL, r, border_radius=4)
            pygame.draw.rect(surf, BLACK, r, 1, border_radius=4)
        # Items
        for f in self.foods:
            f.draw(surf)
        if self.poison:
            self.poison.draw(surf)
        if self.powerup:
            self.powerup.draw(surf)
        self.snake.draw(surf, shielded=self.shield)
        self._draw_hud(surf)

    def _draw_grid(self, surf):
        # Play area background
        pygame.draw.rect(surf, BLACK,
                         (0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT))
        if self.settings.get("grid", True):
            for x in range(0, WIDTH, CELL):
                pygame.draw.line(surf, GRID,
                                 (x, HUD_HEIGHT), (x, HEIGHT))
            for y in range(HUD_HEIGHT, HEIGHT, CELL):
                pygame.draw.line(surf, GRID, (0, y), (WIDTH, y))
        # Border
        pygame.draw.rect(surf, WALL,
                         (0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT), 2)

    def _draw_hud(self, surf):
        pygame.draw.rect(surf, HUD_BG, (0, 0, WIDTH, HUD_HEIGHT))
        pygame.draw.line(surf, WALL, (0, HUD_HEIGHT - 1),
                         (WIDTH, HUD_HEIGHT - 1), 1)
        f = pygame.font.SysFont("arial", 18, bold=True)
        small = pygame.font.SysFont("arial", 14)
        surf.blit(f.render(f"SCORE {self.score}", True, WHITE), (12, 8))
        surf.blit(f.render(f"LV {self.level}", True, GOLD), (12, 32))
        surf.blit(small.render(f"PB {self.personal_best}", True, SILVER),
                  (130, 12))
        surf.blit(small.render(f"{self.username}", True, GREEN),
                  (130, 34))

        # Active effect
        if self.active_effect:
            kind, end = self.active_effect
            remain = max(0, (end - pygame.time.get_ticks()) // 1000 + 1)
            label = "SPEED" if kind == "speed" else "SLOW"
            surf.blit(f.render(f"{label} {remain}s", True, CYAN),
                      (WIDTH - 160, 8))
        if self.shield:
            surf.blit(f.render("SHIELD", True, GOLD),
                      (WIDTH - 160, 32))

        # Power-up on field countdown
        if self.powerup:
            rem = max(0, (POWERUP_FIELD_TTL_MS
                          - (pygame.time.get_ticks() - self.powerup.born_ms)) // 1000 + 1)
            surf.blit(small.render(f"PWR {rem}s", True, ORANGE),
                      (WIDTH - 60, 36))

        if self.flash:
            f2 = pygame.font.SysFont("arial", 22, bold=True)
            text = f2.render(self.flash, True, GOLD)
            tw, th = text.get_size()
            surf.blit(text, ((WIDTH - tw) // 2, HUD_HEIGHT // 2 - th // 2))

    def summary(self):
        return {
            "username":      self.username,
            "score":         int(self.score),
            "level_reached": int(self.level),
            "reason":        self.death_reason,
        }
