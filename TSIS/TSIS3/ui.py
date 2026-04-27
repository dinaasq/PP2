"""UI screens: menu, settings, leaderboard, name entry, game over."""
import pygame

from persistence import (
    CAR_COLORS, DIFFICULTY_PRESETS,
    save_settings, load_leaderboard,
)
from racer import WIDTH, HEIGHT, WHITE, BLACK, ROAD, GRASS, YELLOW, GREEN

TITLE_FONT = ("arial", 56)
HEAD_FONT = ("arial", 30)
BODY_FONT = ("arial", 20)
SMALL_FONT = ("arial", 16)


def font(spec, bold=False):
    return pygame.font.SysFont(spec[0], spec[1], bold=bold)


class Button:
    def __init__(self, rect, label, on_click, color=(40, 40, 50),
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
        f = font(BODY_FONT, bold=True)
        text = f.render(self.label, True, self.text_color)
        tw, th = text.get_size()
        surf.blit(text, (self.rect.centerx - tw // 2,
                         self.rect.centery - th // 2))

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()


def draw_background(surf):
    surf.fill(GRASS)
    pygame.draw.rect(surf, ROAD, (60, 0, WIDTH - 120, HEIGHT))
    for y in range(0, HEIGHT, 40):
        pygame.draw.rect(surf, WHITE, (WIDTH // 2 - 2, y, 4, 22))
    pygame.draw.rect(surf, WHITE, (56, 0, 4, HEIGHT))
    pygame.draw.rect(surf, WHITE, (WIDTH - 60, 0, 4, HEIGHT))


def draw_centered_text(surf, text, y, spec=HEAD_FONT, color=WHITE, bold=True):
    f = font(spec, bold=bold)
    img = f.render(text, True, color)
    tw, th = img.get_size()
    surf.blit(img, ((WIDTH - tw) // 2, y))
    return th


class MainMenu:
    def __init__(self, app):
        self.app = app
        cx = WIDTH // 2
        bw, bh, gap = 240, 56, 14
        y0 = 280
        self.buttons = [
            Button((cx - bw // 2, y0 + (bh + gap) * 0, bw, bh),
                   "PLAY", lambda: app.go("name")),
            Button((cx - bw // 2, y0 + (bh + gap) * 1, bw, bh),
                   "LEADERBOARD", lambda: app.go("leaderboard")),
            Button((cx - bw // 2, y0 + (bh + gap) * 2, bw, bh),
                   "SETTINGS", lambda: app.go("settings")),
            Button((cx - bw // 2, y0 + (bh + gap) * 3, bw, bh),
                   "QUIT", lambda: app.quit()),
        ]

    def handle(self, event):
        for b in self.buttons:
            b.handle(event)

    def draw(self, surf):
        draw_background(surf)
        draw_centered_text(surf, "RACER", 110, TITLE_FONT, YELLOW)
        draw_centered_text(surf, "TSIS 3", 180, BODY_FONT, WHITE)
        draw_centered_text(surf, "Arrow keys to switch lanes",
                           240, SMALL_FONT, (210, 210, 210), bold=False)
        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.draw(surf, mouse)


class NameEntry:
    def __init__(self, app):
        self.app = app
        self.name = ""
        cx = WIDTH // 2
        self.start_btn = Button((cx - 120, 460, 240, 56), "START",
                                self._start, color=(50, 110, 60),
                                hover=(70, 160, 90))
        self.back_btn = Button((cx - 120, 530, 240, 46), "BACK",
                               lambda: app.go("menu"))

    def _start(self):
        if not self.name.strip():
            self.name = "PLAYER"
        self.app.player_name = self.name.strip()[:12]
        self.app.start_game()

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._start()
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.app.go("menu")
            else:
                ch = event.unicode
                if ch and ch.isprintable() and len(self.name) < 12:
                    self.name += ch
        self.start_btn.handle(event)
        self.back_btn.handle(event)

    def draw(self, surf):
        draw_background(surf)
        draw_centered_text(surf, "ENTER NAME", 200, HEAD_FONT, YELLOW)
        # Input box
        box = pygame.Rect((WIDTH - 280) // 2, 280, 280, 60)
        pygame.draw.rect(surf, (25, 25, 30), box, border_radius=8)
        pygame.draw.rect(surf, WHITE, box, 2, border_radius=8)
        f = font(HEAD_FONT, bold=True)
        text = f.render(self.name + ("|" if pygame.time.get_ticks() // 400 % 2 else ""),
                        True, WHITE)
        surf.blit(text, (box.x + 14, box.y + 14))
        draw_centered_text(surf, "Enter to start, Esc to cancel",
                           360, SMALL_FONT, (210, 210, 210), bold=False)
        mouse = pygame.mouse.get_pos()
        self.start_btn.draw(surf, mouse)
        self.back_btn.draw(surf, mouse)


class SettingsScreen:
    def __init__(self, app):
        self.app = app
        self.color_keys = list(CAR_COLORS.keys())
        self.diff_keys = list(DIFFICULTY_PRESETS.keys())
        cx = WIDTH // 2
        self.buttons = [
            Button((cx - 120, 200, 240, 50), self._sound_label(),
                   self.toggle_sound),
            Button((cx - 180, 290, 60, 50), "<", self.prev_color),
            Button((cx + 120, 290, 60, 50), ">", self.next_color),
            Button((cx - 180, 390, 60, 50), "<", self.prev_diff),
            Button((cx + 120, 390, 60, 50), ">", self.next_diff),
            Button((cx - 120, 540, 240, 50), "BACK",
                   lambda: app.go("menu")),
        ]

    def _sound_label(self):
        return f"SOUND: {'ON' if self.app.settings['sound'] else 'OFF'}"

    def toggle_sound(self):
        self.app.settings["sound"] = not self.app.settings["sound"]
        self.buttons[0].label = self._sound_label()
        save_settings(self.app.settings)

    def prev_color(self):
        i = self.color_keys.index(self.app.settings["car_color"])
        self.app.settings["car_color"] = self.color_keys[(i - 1) % len(self.color_keys)]
        save_settings(self.app.settings)

    def next_color(self):
        i = self.color_keys.index(self.app.settings["car_color"])
        self.app.settings["car_color"] = self.color_keys[(i + 1) % len(self.color_keys)]
        save_settings(self.app.settings)

    def prev_diff(self):
        i = self.diff_keys.index(self.app.settings["difficulty"])
        self.app.settings["difficulty"] = self.diff_keys[(i - 1) % len(self.diff_keys)]
        save_settings(self.app.settings)

    def next_diff(self):
        i = self.diff_keys.index(self.app.settings["difficulty"])
        self.app.settings["difficulty"] = self.diff_keys[(i + 1) % len(self.diff_keys)]
        save_settings(self.app.settings)

    def handle(self, event):
        for b in self.buttons:
            b.handle(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.go("menu")

    def draw(self, surf):
        draw_background(surf)
        draw_centered_text(surf, "SETTINGS", 110, HEAD_FONT, YELLOW)

        # Car color preview
        draw_centered_text(surf, "CAR COLOR", 270, BODY_FONT)
        preview = pygame.Rect(WIDTH // 2 - 40, 290, 80, 50)
        pygame.draw.rect(surf, CAR_COLORS[self.app.settings["car_color"]],
                         preview, border_radius=8)
        pygame.draw.rect(surf, WHITE, preview, 2, border_radius=8)
        draw_centered_text(surf, self.app.settings["car_color"].upper(),
                           344, SMALL_FONT, WHITE, bold=False)

        # Difficulty
        draw_centered_text(surf, "DIFFICULTY", 370, BODY_FONT)
        draw_centered_text(surf, self.app.settings["difficulty"].upper(),
                           405, HEAD_FONT, GREEN)

        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.draw(surf, mouse)


class LeaderboardScreen:
    def __init__(self, app):
        self.app = app
        self.entries = load_leaderboard()
        cx = WIDTH // 2
        self.back = Button((cx - 120, HEIGHT - 80, 240, 50), "BACK",
                           lambda: app.go("menu"))

    def refresh(self):
        self.entries = load_leaderboard()

    def handle(self, event):
        self.back.handle(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.app.go("menu")

    def draw(self, surf):
        draw_background(surf)
        draw_centered_text(surf, "TOP 10", 60, HEAD_FONT, YELLOW)

        f_head = font(BODY_FONT, bold=True)
        f_row = font(BODY_FONT, bold=False)
        headers = [("RANK", 30), ("NAME", 100), ("SCORE", 260), ("DIST", 380)]
        for label, x in headers:
            surf.blit(f_head.render(label, True, (220, 220, 220)), (x, 120))

        if not self.entries:
            draw_centered_text(surf, "No scores yet — go race!",
                               260, BODY_FONT, WHITE, bold=False)
        else:
            for i, e in enumerate(self.entries):
                y = 160 + i * 36
                row_bg = pygame.Surface((WIDTH - 40, 32), pygame.SRCALPHA)
                row_bg.fill((0, 0, 0, 90 if i % 2 == 0 else 60))
                surf.blit(row_bg, (20, y - 4))
                cells = [
                    (f"{i + 1}", 30),
                    (e["name"], 100),
                    (f"{e['score']}", 260),
                    (f"{e['distance']}m", 380),
                ]
                for text, x in cells:
                    surf.blit(f_row.render(text, True, WHITE), (x, y))

        mouse = pygame.mouse.get_pos()
        self.back.draw(surf, mouse)


class GameOverScreen:
    def __init__(self, app, summary):
        self.app = app
        self.summary = summary
        cx = WIDTH // 2
        self.buttons = [
            Button((cx - 120, 460, 240, 56), "RETRY",
                   lambda: app.go("name"),
                   color=(50, 110, 60), hover=(70, 160, 90)),
            Button((cx - 120, 530, 240, 56), "MAIN MENU",
                   lambda: app.go("menu")),
        ]

    def handle(self, event):
        for b in self.buttons:
            b.handle(event)

    def draw(self, surf):
        draw_background(surf)
        title = "FINISH!" if self.summary["won"] else "GAME OVER"
        color = GREEN if self.summary["won"] else (230, 80, 80)
        draw_centered_text(surf, title, 110, TITLE_FONT, color)
        if not self.summary["won"] and self.summary["reason"]:
            draw_centered_text(surf, f"Crashed into {self.summary['reason']}",
                               180, BODY_FONT, WHITE, bold=False)

        f = font(HEAD_FONT, bold=True)
        rows = [
            ("DRIVER",   self.summary["name"]),
            ("SCORE",    f"{self.summary['score']}"),
            ("DISTANCE", f"{self.summary['distance']} m"),
            ("COINS",    f"{self.summary['coins']}"),
        ]
        y = 240
        for label, value in rows:
            l = f.render(label, True, (210, 210, 210))
            v = f.render(value, True, YELLOW)
            surf.blit(l, (90, y))
            vw = v.get_width()
            surf.blit(v, (WIDTH - 90 - vw, y))
            y += 44

        mouse = pygame.mouse.get_pos()
        for b in self.buttons:
            b.draw(surf, mouse)
