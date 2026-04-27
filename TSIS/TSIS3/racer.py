"""Racer game core: player, traffic, obstacles, power-ups, scoring."""
import random
import pygame

from persistence import CAR_COLORS, DIFFICULTY_PRESETS

# Window / road geometry
WIDTH, HEIGHT = 480, 720
ROAD_LEFT = 60
ROAD_RIGHT = WIDTH - 60
ROAD_WIDTH = ROAD_RIGHT - ROAD_LEFT
LANES = 4
LANE_WIDTH = ROAD_WIDTH // LANES
LANE_CENTERS = [ROAD_LEFT + LANE_WIDTH // 2 + i * LANE_WIDTH for i in range(LANES)]

# Player
CAR_W, CAR_H = 46, 80
PLAYER_Y = HEIGHT - 110
PLAYER_BASE_SPEED = 6.0       # lateral move speed
WORLD_BASE_SCROLL = 6.0       # forward scroll speed of road

# Finish distance (meters)
FINISH_DISTANCE = 5000

# Colors
WHITE = (240, 240, 240)
BLACK = (15, 15, 15)
ROAD = (45, 45, 50)
GRASS = (38, 110, 60)
LINE = (235, 235, 235)
YELLOW = (240, 210, 60)
RED = (220, 70, 70)
BLUE = (70, 140, 235)
GREEN = (80, 200, 110)
ORANGE = (240, 140, 50)
PURPLE = (170, 90, 210)
GRAY = (110, 110, 115)
DARK = (25, 25, 28)


class Player:
    def __init__(self, color_name):
        self.lane = LANES // 2
        self.x = LANE_CENTERS[self.lane] - CAR_W // 2
        self.y = PLAYER_Y
        self.color = CAR_COLORS.get(color_name, CAR_COLORS["red"])
        self.target_x = self.x
        self.shield = False
        self.repairs = 0

    def move(self, direction):
        new_lane = max(0, min(LANES - 1, self.lane + direction))
        self.lane = new_lane
        self.target_x = LANE_CENTERS[self.lane] - CAR_W // 2

    def update(self):
        # Smoothly slide toward target lane
        if abs(self.x - self.target_x) > 1:
            step = (self.target_x - self.x) * 0.25
            self.x += step
        else:
            self.x = self.target_x

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), CAR_W, CAR_H)

    def draw(self, surf):
        r = self.rect()
        # Body
        pygame.draw.rect(surf, self.color, r, border_radius=8)
        # Windshield
        ws = pygame.Rect(r.x + 6, r.y + 14, r.w - 12, 22)
        pygame.draw.rect(surf, (30, 40, 60), ws, border_radius=4)
        # Tail lights
        pygame.draw.rect(surf, (40, 40, 40), (r.x + 4, r.bottom - 10, 10, 6))
        pygame.draw.rect(surf, (40, 40, 40), (r.right - 14, r.bottom - 10, 10, 6))
        # Wheels
        pygame.draw.rect(surf, BLACK, (r.x - 4, r.y + 10, 6, 18), border_radius=2)
        pygame.draw.rect(surf, BLACK, (r.right - 2, r.y + 10, 6, 18), border_radius=2)
        pygame.draw.rect(surf, BLACK, (r.x - 4, r.bottom - 28, 6, 18), border_radius=2)
        pygame.draw.rect(surf, BLACK, (r.right - 2, r.bottom - 28, 6, 18), border_radius=2)
        # Shield aura
        if self.shield:
            pygame.draw.ellipse(surf, (90, 200, 255),
                                r.inflate(20, 16), 3)


class Entity:
    """Base for anything scrolling down the road."""
    def __init__(self, lane, y, w, h):
        self.lane = lane
        self.x = LANE_CENTERS[lane] - w // 2
        self.y = y
        self.w = w
        self.h = h
        self.alive = True

    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, scroll):
        self.y += scroll
        if self.y > HEIGHT + 20:
            self.alive = False


class TrafficCar(Entity):
    COLORS = [(200, 60, 60), (60, 100, 200), (220, 180, 60),
              (160, 160, 160), (120, 60, 180), (80, 200, 130)]

    def __init__(self, lane, y, extra_speed=0.0):
        super().__init__(lane, y, CAR_W, CAR_H)
        self.color = random.choice(self.COLORS)
        self.extra_speed = extra_speed   # moves with the world a bit slower

    def update(self, scroll):
        # Traffic moves downward but slower than world scroll, simulating drive
        super().update(scroll - self.extra_speed)

    def draw(self, surf):
        r = self.rect()
        pygame.draw.rect(surf, self.color, r, border_radius=8)
        ws = pygame.Rect(r.x + 6, r.y + 14, r.w - 12, 22)
        pygame.draw.rect(surf, (30, 40, 60), ws, border_radius=4)
        pygame.draw.rect(surf, (40, 40, 40), (r.x + 4, r.y + 4, 10, 6))
        pygame.draw.rect(surf, (40, 40, 40), (r.right - 14, r.y + 4, 10, 6))


class Obstacle(Entity):
    """Static road hazards: barrier, oil spill, pothole, speed bump, nitro strip."""
    KINDS = ("barrier", "oil", "pothole", "bump", "nitro")

    def __init__(self, lane, y, kind):
        w = LANE_WIDTH - 16
        h = 36 if kind in ("barrier", "bump", "nitro") else 44
        super().__init__(lane, y, w, h)
        self.kind = kind

    def draw(self, surf):
        r = self.rect()
        if self.kind == "barrier":
            pygame.draw.rect(surf, ORANGE, r, border_radius=4)
            for i in range(0, r.w, 12):
                pygame.draw.rect(surf, BLACK, (r.x + i, r.y, 6, r.h))
        elif self.kind == "oil":
            pygame.draw.ellipse(surf, (10, 10, 14), r)
            pygame.draw.ellipse(surf, (40, 40, 50), r.inflate(-12, -10), 2)
        elif self.kind == "pothole":
            pygame.draw.ellipse(surf, BLACK, r)
            pygame.draw.ellipse(surf, (60, 60, 60), r.inflate(-10, -6), 2)
        elif self.kind == "bump":
            pygame.draw.rect(surf, (220, 200, 60), r, border_radius=6)
            pygame.draw.rect(surf, BLACK, r, 2, border_radius=6)
            for i in range(8, r.w - 8, 14):
                pygame.draw.line(surf, BLACK, (r.x + i, r.y + 4),
                                 (r.x + i, r.bottom - 4), 2)
        elif self.kind == "nitro":
            pygame.draw.rect(surf, (60, 220, 240), r, border_radius=6)
            pygame.draw.polygon(surf, WHITE, [
                (r.centerx - 8, r.y + 6),
                (r.centerx + 8, r.centery),
                (r.centerx - 4, r.centery),
                (r.centerx + 8, r.bottom - 6),
                (r.centerx - 8, r.centery + 4),
                (r.centerx + 4, r.centery - 2),
            ])


class MovingBarrier(Entity):
    """Barrier that drifts horizontally inside its lane area."""
    def __init__(self, lane, y):
        w = LANE_WIDTH - 20
        super().__init__(lane, y, w, 30)
        self.dir = random.choice([-1, 1])
        self.lane_left = ROAD_LEFT + lane * LANE_WIDTH + 4
        self.lane_right = self.lane_left + LANE_WIDTH - 8 - w

    def update(self, scroll):
        super().update(scroll)
        self.x += self.dir * 1.6
        if self.x < self.lane_left:
            self.x = self.lane_left
            self.dir *= -1
        if self.x > self.lane_right:
            self.x = self.lane_right
            self.dir *= -1

    def draw(self, surf):
        r = self.rect()
        pygame.draw.rect(surf, (240, 240, 240), r, border_radius=4)
        for i in range(0, r.w, 14):
            pygame.draw.rect(surf, RED, (r.x + i, r.y, 7, r.h))


class PowerUp(Entity):
    KINDS = ("nitro", "shield", "repair")

    def __init__(self, lane, y, kind):
        super().__init__(lane, y, 34, 34)
        self.kind = kind
        self.life = 600  # frames before despawn if not collected

    def update(self, scroll):
        super().update(scroll)
        self.life -= 1
        if self.life <= 0:
            self.alive = False

    def draw(self, surf):
        r = self.rect()
        if self.kind == "nitro":
            pygame.draw.rect(surf, (60, 220, 240), r, border_radius=8)
            pygame.draw.polygon(surf, WHITE, [
                (r.centerx - 6, r.y + 6),
                (r.centerx + 8, r.centery - 2),
                (r.centerx - 2, r.centery),
                (r.centerx + 6, r.bottom - 6),
            ])
        elif self.kind == "shield":
            pygame.draw.rect(surf, (90, 160, 240), r, border_radius=8)
            pygame.draw.polygon(surf, WHITE, [
                (r.centerx, r.y + 5),
                (r.right - 5, r.y + 12),
                (r.right - 8, r.bottom - 6),
                (r.centerx, r.bottom - 4),
                (r.x + 8, r.bottom - 6),
                (r.x + 5, r.y + 12),
            ], 2)
        else:  # repair
            pygame.draw.rect(surf, GREEN, r, border_radius=8)
            pygame.draw.rect(surf, WHITE, (r.centerx - 3, r.y + 7, 6, r.h - 14))
            pygame.draw.rect(surf, WHITE, (r.x + 7, r.centery - 3, r.w - 14, 6))


# Coin from previous practice (kept here so file is self-contained)
class Coin(Entity):
    def __init__(self, lane, y):
        super().__init__(lane, y, 22, 22)
        # Weighted coin values from Practice 11
        self.value = random.choices([1, 5, 10], weights=[70, 25, 5])[0]
        self.color = {1: (235, 200, 60), 5: (220, 220, 220), 10: (210, 130, 40)}[self.value]

    def draw(self, surf):
        r = self.rect()
        pygame.draw.circle(surf, self.color, r.center, r.w // 2)
        pygame.draw.circle(surf, BLACK, r.center, r.w // 2, 2)


class Game:
    """Holds full game state for one run."""

    def __init__(self, settings, player_name):
        self.settings = settings
        self.player_name = player_name or "PLAYER"
        preset = DIFFICULTY_PRESETS[settings["difficulty"]]
        self.spawn_rate = preset["spawn_rate"]
        self.obstacle_rate = preset["obstacle_rate"]
        self.enemy_speed = preset["start_enemy_speed"]
        self.player = Player(settings["car_color"])

        self.coins = []
        self.traffic = []
        self.obstacles = []
        self.powerups = []

        self.coin_count = 0
        self.score = 0
        self.distance = 0.0
        self.line_offset = 0.0

        self.active_powerup = None       # ("nitro", frames_left) or ("shield", -1) etc.
        self.nitro_frames = 0
        self.message = ""
        self.message_frames = 0

        self.game_over = False
        self.won = False
        self.crash_reason = ""

    # ---------- spawning ----------

    def _free_lane(self, exclude_player_zone=True):
        """Pick a lane not occupied near the top, preferring not the player's."""
        candidates = list(range(LANES))
        random.shuffle(candidates)
        for lane in candidates:
            occupied = False
            for ent in self.traffic + self.obstacles + self.powerups + self.coins:
                if ent.lane == lane and ent.y < 180:
                    occupied = True
                    break
            if exclude_player_zone and lane == self.player.lane and self.player.y - 220 < 0:
                # Avoid spawning right above player's lane while close to top
                pass
            if not occupied:
                return lane
        return None

    def _spawn_traffic(self):
        if random.random() < self.spawn_rate:
            lane = self._free_lane()
            if lane is None:
                return
            extra = random.uniform(0.5, 2.0)
            self.traffic.append(TrafficCar(lane, -CAR_H, extra_speed=extra))

    def _spawn_obstacle(self):
        if random.random() < self.obstacle_rate:
            lane = self._free_lane()
            if lane is None:
                return
            kind = random.choices(
                Obstacle.KINDS,
                weights=[20, 25, 20, 20, 15],
            )[0]
            self.obstacles.append(Obstacle(lane, -50, kind))
        if random.random() < self.obstacle_rate * 0.35:
            lane = self._free_lane()
            if lane is None:
                return
            self.obstacles.append(MovingBarrier(lane, -40))

    def _spawn_coin(self):
        if random.random() < 0.025:
            lane = self._free_lane()
            if lane is None:
                return
            self.coins.append(Coin(lane, -30))

    def _spawn_powerup(self):
        if random.random() < 0.0035:
            lane = self._free_lane()
            if lane is None:
                return
            kind = random.choice(PowerUp.KINDS)
            self.powerups.append(PowerUp(lane, -40, kind))

    # ---------- update ----------

    def handle_input(self, event):
        if self.game_over:
            return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.player.move(-1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.player.move(1)

    def update(self):
        if self.game_over:
            return

        # Difficulty scaling: every 500m, traffic and obstacles get tougher
        scaling = 1.0 + (self.distance / 500.0) * 0.05
        spawn_rate = min(0.12, self.spawn_rate * scaling)
        self.spawn_rate_current = spawn_rate

        # World scroll, boosted if nitro
        scroll = WORLD_BASE_SCROLL + (self.distance / 1500.0)
        if self.nitro_frames > 0:
            scroll *= 1.8
            self.nitro_frames -= 1
            if self.nitro_frames == 0 and self.active_powerup and self.active_powerup[0] == "nitro":
                self.active_powerup = None

        # Distance & dashed lines
        self.distance += scroll * 0.25
        self.line_offset = (self.line_offset + scroll) % 40

        # Spawning
        self._spawn_traffic()
        self._spawn_obstacle()
        self._spawn_coin()
        self._spawn_powerup()

        # Update entities
        self.player.update()
        for group in (self.traffic, self.obstacles, self.powerups, self.coins):
            for ent in group:
                ent.update(scroll)
            group[:] = [e for e in group if e.alive]

        # Collisions
        pr = self.player.rect()

        # Coins
        for c in self.coins:
            if pr.colliderect(c.rect()):
                c.alive = False
                self.coin_count += c.value
                self.score += c.value * 10
                # From practice 11: enemy speed grows after collecting coins
                self.enemy_speed += 0.05

        # Power-ups
        for p in self.powerups:
            if pr.colliderect(p.rect()):
                p.alive = False
                self._apply_powerup(p.kind)

        # Obstacles
        for o in list(self.obstacles):
            if pr.colliderect(o.rect()):
                if o.kind == "nitro":
                    o.alive = False
                    self._apply_powerup("nitro")
                    self._flash("NITRO STRIP!")
                elif o.kind == "bump":
                    o.alive = False
                    self.score = max(0, self.score - 20)
                    self._flash("SPEED BUMP -20")
                elif o.kind == "oil":
                    o.alive = False
                    # Random sideways slide
                    self.player.move(random.choice([-1, 1]))
                    self._flash("OIL SLIP!")
                else:
                    self._handle_crash(o.kind.upper())
                    o.alive = False

        # Traffic collisions
        for t in self.traffic:
            if pr.colliderect(t.rect()):
                self._handle_crash("TRAFFIC")
                t.alive = False
                break

        # Score from distance
        self.score = int(self.score + scroll * 0.05)

        # Win condition
        if self.distance >= FINISH_DISTANCE:
            self.game_over = True
            self.won = True
            self.score += 500  # finish bonus

        # Flash timer
        if self.message_frames > 0:
            self.message_frames -= 1
            if self.message_frames == 0:
                self.message = ""

    def _apply_powerup(self, kind):
        if kind == "nitro":
            self.nitro_frames = 60 * 4   # 4 seconds at 60fps
            self.active_powerup = ("nitro", self.nitro_frames)
            self._flash("NITRO!")
        elif kind == "shield":
            self.player.shield = True
            self.active_powerup = ("shield", -1)
            self._flash("SHIELD!")
        elif kind == "repair":
            self.player.repairs += 1
            self.active_powerup = ("repair", 60)
            self._flash("REPAIR +1")

    def _handle_crash(self, source):
        if self.player.shield:
            self.player.shield = False
            if self.active_powerup and self.active_powerup[0] == "shield":
                self.active_powerup = None
            self._flash(f"SHIELD ABSORBED {source}")
            return
        if self.player.repairs > 0:
            self.player.repairs -= 1
            self._flash(f"REPAIR USED ({source})")
            return
        self.game_over = True
        self.crash_reason = source

    def _flash(self, text):
        self.message = text
        self.message_frames = 90

    # ---------- draw ----------

    def draw(self, surf):
        # Grass
        surf.fill(GRASS)
        # Road
        pygame.draw.rect(surf, ROAD, (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT))
        # Road edge stripes
        pygame.draw.rect(surf, WHITE, (ROAD_LEFT - 4, 0, 4, HEIGHT))
        pygame.draw.rect(surf, WHITE, (ROAD_RIGHT, 0, 4, HEIGHT))
        # Lane dividers (dashed)
        for i in range(1, LANES):
            x = ROAD_LEFT + i * LANE_WIDTH
            y = -40 + int(self.line_offset)
            while y < HEIGHT:
                pygame.draw.rect(surf, LINE, (x - 2, y, 4, 22))
                y += 40

        # Entities
        for c in self.coins:
            c.draw(surf)
        for o in self.obstacles:
            o.draw(surf)
        for p in self.powerups:
            p.draw(surf)
        for t in self.traffic:
            t.draw(surf)
        self.player.draw(surf)

        self._draw_hud(surf)

    def _draw_hud(self, surf):
        font = pygame.font.SysFont("arial", 18, bold=True)
        small = pygame.font.SysFont("arial", 14)

        # Top translucent bar
        bar = pygame.Surface((WIDTH, 64), pygame.SRCALPHA)
        bar.fill((0, 0, 0, 130))
        surf.blit(bar, (0, 0))

        surf.blit(font.render(f"SCORE {self.score}", True, WHITE), (12, 8))
        surf.blit(font.render(f"COINS {self.coin_count}", True, YELLOW), (12, 32))
        surf.blit(font.render(f"{int(self.distance)} m", True, WHITE), (WIDTH - 100, 8))
        remaining = max(0, FINISH_DISTANCE - int(self.distance))
        surf.blit(small.render(f"to finish: {remaining} m", True, WHITE),
                  (WIDTH - 130, 36))

        # Distance bar
        bar_w = 200
        x = (WIDTH - bar_w) // 2
        pygame.draw.rect(surf, (60, 60, 60), (x, 16, bar_w, 10), border_radius=4)
        pct = min(1.0, self.distance / FINISH_DISTANCE)
        pygame.draw.rect(surf, GREEN, (x, 16, int(bar_w * pct), 10), border_radius=4)

        # Active power-up
        if self.active_powerup:
            kind, frames = self.active_powerup
            label = kind.upper()
            if kind == "nitro":
                label += f"  {self.nitro_frames // 60 + 1}s"
            elif kind == "shield":
                label += "  ON"
            elif kind == "repair":
                label += f"  x{self.player.repairs}"
            surf.blit(font.render(label, True, (90, 220, 240)),
                      ((WIDTH - 160) // 2, 32))

        # Repairs always shown
        if self.player.repairs > 0 and (
            not self.active_powerup or self.active_powerup[0] != "repair"
        ):
            surf.blit(small.render(f"REPAIRS x{self.player.repairs}", True, GREEN),
                      (WIDTH - 130, 50))

        # Flash message
        if self.message:
            f2 = pygame.font.SysFont("arial", 26, bold=True)
            text = f2.render(self.message, True, YELLOW)
            tw, th = text.get_size()
            bg = pygame.Surface((tw + 20, th + 10), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 140))
            surf.blit(bg, ((WIDTH - tw - 20) // 2, HEIGHT // 2 - 30))
            surf.blit(text, ((WIDTH - tw) // 2, HEIGHT // 2 - 25))

    def summary(self):
        return {
            "name": self.player_name,
            "score": int(self.score),
            "distance": int(self.distance),
            "coins": int(self.coin_count),
            "won": self.won,
            "reason": self.crash_reason,
        }
