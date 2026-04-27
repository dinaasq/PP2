# 🐍 TSIS 4: Snake Game — Database Integration & Advanced Gameplay

## 📌 Description

This project is an advanced **Snake game built with Pygame** and integrated with **PostgreSQL database (psycopg2)**.

It extends the classic Snake game with:
- persistent leaderboard
- power-ups system
- poison food mechanic
- obstacles and level scaling
- full menu system and settings storage

The main focus is combining **game development + database persistence**.

---

## ⚙️ Technologies

- Python 3
- Pygame
- PostgreSQL
- psycopg2
- JSON (settings storage)

---

## 🧱 Base Features (from Practice 10–11)

- Wall/border collision detection
- Random food placement (avoiding snake & walls)
- Level progression system
- Speed increase per level
- Score and level display
- Weighted food (different point values)
- Timed disappearing food

---

## 🗄️ Database Integration (PostgreSQL)

### 📁 Tables

```sql id="snake_db_1"
CREATE TABLE players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);
CREATE TABLE game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER NOT NULL,
    level_reached INTEGER NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);

Project Structure
TSIS4/
├── main.py
├── game.py
├── db.py
├── config.py
├── settings.json
└── assets/
    ├── sounds/
    └── images/
``` id="snake_struct"

---

## 🚀 How to Run

```bash
pip install pygame psycopg2
python main.py