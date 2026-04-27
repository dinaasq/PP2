"""Persistence layer: load/save settings and leaderboard JSON files."""
import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "red",
    "difficulty": "normal",
}

DIFFICULTY_PRESETS = {
    "easy":   {"start_enemy_speed": 3.0, "spawn_rate": 0.012, "obstacle_rate": 0.004},
    "normal": {"start_enemy_speed": 4.5, "spawn_rate": 0.020, "obstacle_rate": 0.007},
    "hard":   {"start_enemy_speed": 6.0, "spawn_rate": 0.030, "obstacle_rate": 0.011},
}

CAR_COLORS = {
    "red":    (220, 40, 40),
    "blue":   (50, 110, 230),
    "green":  (60, 180, 90),
    "yellow": (235, 200, 60),
    "purple": (160, 80, 200),
}


def load_settings():
    """Read settings.json and merge with defaults."""
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return dict(DEFAULT_SETTINGS)
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        merged = dict(DEFAULT_SETTINGS)
        merged.update({k: v for k, v in data.items() if k in DEFAULT_SETTINGS})
        if merged["car_color"] not in CAR_COLORS:
            merged["car_color"] = "red"
        if merged["difficulty"] not in DIFFICULTY_PRESETS:
            merged["difficulty"] = "normal"
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


def load_leaderboard():
    """Return list of leaderboard entries sorted by score desc."""
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        cleaned = []
        for entry in data:
            if not isinstance(entry, dict):
                continue
            cleaned.append({
                "name":     str(entry.get("name", "PLAYER"))[:12],
                "score":    int(entry.get("score", 0)),
                "distance": int(entry.get("distance", 0)),
                "coins":    int(entry.get("coins", 0)),
            })
        cleaned.sort(key=lambda e: e["score"], reverse=True)
        return cleaned
    except (json.JSONDecodeError, OSError, ValueError):
        return []


def save_leaderboard(entries):
    """Save leaderboard entries to leaderboard.json (top 10 only)."""
    try:
        trimmed = sorted(entries, key=lambda e: e["score"], reverse=True)[:10]
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(trimmed, f, indent=2)
    except OSError:
        pass


def add_score(name, score, distance, coins):
    """Insert a run into leaderboard and return updated top 10."""
    entries = load_leaderboard()
    entries.append({
        "name":     (name or "PLAYER").strip()[:12] or "PLAYER",
        "score":    int(score),
        "distance": int(distance),
        "coins":    int(coins),
    })
    entries.sort(key=lambda e: e["score"], reverse=True)
    entries = entries[:10]
    save_leaderboard(entries)
    return entries
