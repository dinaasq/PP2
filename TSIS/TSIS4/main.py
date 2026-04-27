"""TSIS 4 — Snake Game with PostgreSQL leaderboard.

Entry point: builds the screens, owns the main loop, and routes events.
"""
import sys
import pygame

from config import (
    WIDTH, HEIGHT, FPS,
    BLACK, WHITE, HUD_BG, GOLD, GREEN, RED, CYAN, BLUE, GRID,
    SNAKE_COLOR_PRESETS, load_settings, save_settings,
)
from db import Database
from game import Game


# ----------------- UI helpers -----------------

def font(size, bold=False):
    return pygame.font.SysFont("arial", size, bold=bold)


class Button:
    def __init__(self, rect, label, on_click, color=(40, 40, 55),
                 hover=(70, 90, 150), text_color=WHITE):
        self.rect = pygame.Rect(rect)
        self.label = label
        self.on_click = on_click
        self.color = color
        self.hover = hover
        self.text_color = text_color

    def draw(self, surf, mouse):
        active = self.rect.collidepoint(mouse)
        pygame.draw.rect(surf, self.hover if active else self.color,
                         self.rect, border_radius=10)
        pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=10)
        f = font(20, bold=True)
        text = f.render(self.label, True, self.text_color)
        tw, th = text.get_size()
        surf.blit(text, (self.rect.centerx - tw // 2,
                         self.rect.centery - th // 2))

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()


def draw_centered(surf, text, y, size=28, color=WHITE, bold=True):
    f = font(size, bold=bold)
    img = f.render(text, True, color)
    tw, th = img.get_size()
    surf.blit(img, ((WIDTH - tw) // 2, y))
    return th


def draw_background(surf):
    surf.fill(BLACK)
    # Light grid backdrop for nice menu look
    for x in range(0, WIDTH, 24):
        pygame.draw.line(surf, GRID, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, 24):
        pygame.draw.line(surf, GRID, (0, y), (WIDTH, y))


# ----------------- Screens -----------------

class MainMenu:
    def __init__(self, app):
        self.app = app
        cx = WIDTH // 2
        # Username input box
        self.input_rect = pygame.Rect(cx - 140, 220, 280, 56)
        bw, bh, gap = 240, 50, 12
        y0 = 330
        self.buttons = [
            Button((cx - bw // 2, y0 + (bh + gap) * 0, bw, bh),
                   "PLAY", self._play,
                   color=(45, 110, 60), hover=(70, 160, 90)),
            Button((cx - bw // 2, y0 + (bh + gap) * 1, bw, bh),
                   "LEADERBOARD", lambda: app.go("leaderboard")),
            Button((cx - bw // 2, y0 + (bh + gap) * 2, bw, bh),
                   "SETTINGS", lambda: app.go("settings")),
            Button((cx - bw // 2, y0 + (bh + gap) * 3, bw, bh),
                   "QUIT", lambda: app.quit()),
        ]

    def _play(self):
        if not self.app.username.strip():
            self.app.username = "PLAYER"
        self.app.start_game()

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._play()
            elif event.key == pygame.K_BACKSPACE:
                self.app.username = self.app.username[:-1]
            else:
                ch = event.unicode
                if ch and ch.isprintable() and len(self.app.username) < 20:
                    self.app.username += ch
        for b in self.buttons:
            b.handle(event)

    def draw(self, surf):
        draw_background(surf)
        draw_centered(surf, "SNAKE", 80, 64, GREEN)
        draw_centered(surf, "TSIS 4 — DB Leaderboard Edition",
                      150, 18, WHITE, bold=False)
        draw_centered(surf, "USERNAME", 190, 18, GOLD)

        # Input box
        pygame.draw.rect(surf, HUD_BG, self.input_rect, border_radius=8)
        pygame.draw.rect(surf, WHITE, self.input_rect, 2, border_radius=8)
        f = font(28, bold=True)
        cursor = "|" if pygame.time.get_ticks() // 400 % 2 else " "
        text = f.render(self.app.username + cursor, True, WHITE)
        surf.blit(text,
                  (self.input_rect.x + 14, self.input_rect.y + 12))

        # DB status
        if self.app.db.available:
            msg, col = "Database: connected", GREEN
        else:
            msg, col = f"Database: OFFLINE ({self.app.db.error or 'no connection'})", RED
        f2 = font(14)
        img = f2.render(msg, True, col)
        surf.blit(img, ((WIDTH - img.get_width()) // 2, HEIGHT - 28))

        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.draw(surf, mouse)


class SettingsScreen:
    def __init__(self, app):
        self.app = app
        self.color_idx = self._initial_color_idx()
        cx = WIDTH // 2
        self.buttons = [
            Button((cx - 140, 180, 280, 50), self._grid_label(),
                   self.toggle_grid),
            Button((cx - 140, 250, 280, 50), self._sound_label(),
                   self.toggle_sound),
            Button((cx - 200, 360, 60, 50), "<", self.prev_color),
            Button((cx + 140, 360, 60, 50), ">", self.next_color),
            Button((cx - 140, 480, 280, 56), "SAVE & BACK",
                   self.save_back, color=(45, 110, 60), hover=(70, 160, 90)),
        ]

    def _initial_color_idx(self):
        cur = self.app.settings["snake_color"]
        for i, (_, c) in enumerate(SNAKE_COLOR_PRESETS):
            if c == cur:
                return i
        return 0

    def _grid_label(self):
        return f"GRID: {'ON' if self.app.settings['grid'] else 'OFF'}"

    def _sound_label(self):
        return f"SOUND: {'ON' if self.app.settings['sound'] else 'OFF'}"

    def toggle_grid(self):
        self.app.settings["grid"] = not self.app.settings["grid"]
        self.buttons[0].label = self._grid_label()

    def toggle_sound(self):
        self.app.settings["sound"] = not self.app.settings["sound"]
        self.buttons[1].label = self._sound_label()
        self.app.apply_sound()

    def prev_color(self):
        self.color_idx = (self.color_idx - 1) % len(SNAKE_COLOR_PRESETS)
        self.app.settings["snake_color"] = list(SNAKE_COLOR_PRESETS[self.color_idx][1])

    def next_color(self):
        self.color_idx = (self.color_idx + 1) % len(SNAKE_COLOR_PRESETS)
        self.app.settings["snake_color"] = list(SNAKE_COLOR_PRESETS[self.color_idx][1])

    def save_back(self):
        save_settings(self.app.settings)
        self.app.go("menu")

    def handle(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.save_back()
        for b in self.buttons:
            b.handle(event)

    def draw(self, surf):
        draw_background(surf)
        draw_centered(surf, "SETTINGS", 90, 36, GOLD)

        # Color preview row
        draw_centered(surf, "SNAKE COLOR", 330, 18, WHITE)
        name = SNAKE_COLOR_PRESETS[self.color_idx][0]
        col = tuple(SNAKE_COLOR_PRESETS[self.color_idx][1])
        preview = pygame.Rect(WIDTH // 2 - 60, 360, 120, 50)
        pygame.draw.rect(surf, col, preview, border_radius=8)
        pygame.draw.rect(surf, WHITE, preview, 2, border_radius=8)
        draw_centered(surf, name, 416, 16, WHITE, bold=False)

        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.draw(surf, mouse)


class LeaderboardScreen:
    def __init__(self, app):
        self.app = app
        self.entries = []
        self.error = ""
        cx = WIDTH // 2
        self.back = Button((cx - 120, HEIGHT - 70, 240, 50),
                           "BACK", lambda: app.go("menu"))

    def refresh(self):
        if self.app.db.available:
            self.entries = self.app.db.top_scores(10)
            self.error = "" if self.entries or not self.app.db.error else self.app.db.error
        else:
            self.entries = []
            self.error = self.app.db.error or "Database offline"

    def handle(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.go("menu")
        self.back.handle(event)

    def draw(self, surf):
        draw_background(surf)
        draw_centered(surf, "TOP 10", 40, 36, GOLD)

        head_f = font(16, bold=True)
        row_f = font(16)
        # Column x positions
        cols = [("RANK", 30), ("NAME", 90), ("SCORE", 280),
                ("LV", 380), ("DATE", 440)]
        for label, x in cols:
            surf.blit(head_f.render(label, True, CYAN), (x, 110))

        if self.error:
            draw_centered(surf, self.error, 230, 16, RED, bold=False)
        elif not self.entries:
            draw_centered(surf, "No scores yet — go play!",
                          230, 18, WHITE, bold=False)
        else:
            for i, e in enumerate(self.entries):
                y = 145 + i * 32
                bg = pygame.Surface((WIDTH - 40, 28), pygame.SRCALPHA)
                bg.fill((255, 255, 255, 18 if i % 2 == 0 else 8))
                surf.blit(bg, (20, y - 4))
                date_str = ""
                played = e.get("played_at")
                if played is not None:
                    try:
                        date_str = played.strftime("%Y-%m-%d")
                    except AttributeError:
                        date_str = str(played)[:10]
                row = [
                    (str(i + 1), 30),
                    (e["username"][:18], 90),
                    (str(e["score"]), 280),
                    (str(e["level_reached"]), 380),
                    (date_str, 440),
                ]
                for text, x in row:
                    surf.blit(row_f.render(text, True, WHITE), (x, y))

        self.back.draw(surf, pygame.mouse.get_pos())


class GameOverScreen:
    def __init__(self, app, summary, personal_best, saved):
        self.app = app
        self.summary = summary
        self.personal_best = personal_best
        self.saved = saved
        cx = WIDTH // 2
        self.buttons = [
            Button((cx - 240, HEIGHT - 110, 220, 56), "RETRY",
                   lambda: app.start_game(),
                   color=(45, 110, 60), hover=(70, 160, 90)),
            Button((cx + 20, HEIGHT - 110, 220, 56),
                   "MAIN MENU", lambda: app.go("menu")),
        ]

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.app.start_game()
            elif event.key == pygame.K_ESCAPE:
                self.app.go("menu")
        for b in self.buttons:
            b.handle(event)

    def draw(self, surf):
        draw_background(surf)
        draw_centered(surf, "GAME OVER", 90, 48, RED)
        if self.summary["reason"]:
            draw_centered(surf, f"Cause: {self.summary['reason']}",
                          150, 16, WHITE, bold=False)

        f = font(26, bold=True)
        rows = [
            ("PLAYER",        self.summary["username"]),
            ("SCORE",         str(self.summary["score"])),
            ("LEVEL REACHED", str(self.summary["level_reached"])),
            ("PERSONAL BEST", str(self.personal_best)),
        ]
        y = 220
        for label, value in rows:
            l = f.render(label, True, (210, 210, 210))
            v = f.render(value, True, GOLD)
            surf.blit(l, (60, y))
            surf.blit(v, (WIDTH - 60 - v.get_width(), y))
            y += 44

        msg = "Saved to leaderboard" if self.saved else "Not saved (DB offline)"
        col = GREEN if self.saved else RED
        draw_centered(surf, msg, y + 10, 16, col, bold=False)

        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.draw(surf, mouse)


# ----------------- App -----------------

class App:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except pygame.error:
            pass
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS 4 — Snake")
        self.clock = pygame.time.Clock()
        self.settings = load_settings()
        self.db = Database()
        self.username = ""
        self.game = None
        self.state = "menu"
        self.screens = {
            "menu":        MainMenu(self),
            "settings":    SettingsScreen(self),
            "leaderboard": LeaderboardScreen(self),
        }
        self.apply_sound()

    def apply_sound(self):
        try:
            vol = 1.0 if self.settings["sound"] else 0.0
            pygame.mixer.music.set_volume(vol)
        except pygame.error:
            pass

    def go(self, state):
        self.state = state
        if state == "menu":
            self.screens["menu"] = MainMenu(self)
        elif state == "settings":
            self.screens["settings"] = SettingsScreen(self)
        elif state == "leaderboard":
            self.screens["leaderboard"].refresh()

    def start_game(self):
        name = self.username.strip() or "PLAYER"
        self.username = name
        pb = self.db.personal_best(name) if self.db.available else 0
        self.game = Game(self.settings, name, personal_best=pb)
        self.state = "play"

    def quit(self):
        self.db.close()
        pygame.quit()
        sys.exit(0)

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if self.state == "play":
                    if event.type == pygame.KEYDOWN:
                        if event.key in (pygame.K_LEFT, pygame.K_a):
                            self.game.turn(-1, 0)
                        elif event.key in (pygame.K_RIGHT, pygame.K_d):
                            self.game.turn(1, 0)
                        elif event.key in (pygame.K_UP, pygame.K_w):
                            self.game.turn(0, -1)
                        elif event.key in (pygame.K_DOWN, pygame.K_s):
                            self.game.turn(0, 1)
                        elif event.key == pygame.K_ESCAPE:
                            self.go("menu")
                else:
                    self.screens.get(self.state, self.screens["menu"]).handle(event)

            if self.state == "play" and self.game:
                self.game.update(dt)
                self.game.draw(self.screen)
                if self.game.game_over:
                    summary = self.game.summary()
                    saved = self.db.save_session(
                        summary["username"],
                        summary["score"],
                        summary["level_reached"],
                    )
                    pb = self.db.personal_best(summary["username"]) \
                        if self.db.available else summary["score"]
                    self.screens["gameover"] = GameOverScreen(
                        self, summary, pb, saved
                    )
                    self.state = "gameover"
                    self.game = None
            else:
                screen = self.screens.get(self.state)
                if screen is None:
                    self.go("menu")
                    screen = self.screens["menu"]
                screen.draw(self.screen)

            pygame.display.flip()


if __name__ == "__main__":
    App().run()
