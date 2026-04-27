"""Game-wide constants and shared helpers."""
import json
import os

# Window / grid
CELL = 24
COLS = 28
ROWS = 22
HUD_HEIGHT = 60
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + HUD_HEIGHT
FPS = 60

# Colors
BLACK = (15, 15, 20)
WHITE = (240, 240, 240)
GRID = (40, 40, 50)
WALL = (90, 90, 110)
RED = (220, 70, 70)
DARK_RED = (130, 25, 25)
GOLD = (235, 200, 60)
SILVER = (200, 200, 210)
GREEN = (80, 200, 110)
BLUE = (70, 140, 235)
CYAN = (60, 220, 240)
PURPLE = (170, 90, 210)
ORANGE = (240, 140, 50)
HUD_BG = (25, 25, 32)

# Snake
START_LENGTH = 4
BASE_SPEED = 8.0          # cells per second at level 1
SPEED_PER_LEVEL = 1.2     # cells per second added per level
FOOD_PER_LEVEL = 5        # eat this many normal foods to level up

# Power-up timings (milliseconds)
POWERUP_FIELD_TTL_MS = 8000   # disappears if not picked up
POWERUP_EFFECT_MS = 5000      # nitro / slow last 5 s
SPEED_BOOST_MULT = 1.7
SLOW_MOTION_MULT = 0.55

# Food timings
FOOD_TTL_MS = 9000            # weighted food despawn (Practice 11 base)
POISON_TTL_MS = 7000

# Obstacles
OBSTACLES_FROM_LEVEL = 3
OBSTACLES_PER_LEVEL = 4       # added each new level >= 3 (max grows)
OBSTACLE_MAX = 30

# Settings file
SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "snake_color": [80, 200, 110],
    "grid": True,
    "sound": True,
}

# Snake color palette (for the settings cycle button)
SNAKE_COLOR_PRESETS = [
    ("Green",  [80, 200, 110]),
    ("Cyan",   [60, 220, 240]),
    ("Blue",   [70, 140, 235]),
    ("Purple", [170, 90, 210]),
    ("Gold",   [235, 200, 60]),
    ("Red",    [220, 70, 70]),
]


def load_settings():
    """Read settings.json and merge with defaults."""
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return dict(DEFAULT_SETTINGS)
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        merged = dict(DEFAULT_SETTINGS)
        for k in DEFAULT_SETTINGS:
            if k in data:
                merged[k] = data[k]
        # Sanity check the color
        c = merged["snake_color"]
        if (not isinstance(c, list) or len(c) != 3
                or not all(isinstance(v, int) and 0 <= v <= 255 for v in c)):
            merged["snake_color"] = list(DEFAULT_SETTINGS["snake_color"])
        return merged
    except (json.JSONDecodeError, OSError):
        return dict(DEFAULT_SETTINGS)


def save_settings(settings):
    """Persist settings dict to settings.json."""
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
    except OSError:
        pass
