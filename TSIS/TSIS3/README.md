# 🏎 TSIS 3: Racer Game — Advanced Driving, Leaderboard & Power-Ups

## 📌 Description

This project is an advanced **arcade-style Racer game built with Pygame**.

It extends previous versions by adding:
- dynamic road hazards
- traffic AI
- power-ups system
- score + distance tracking
- persistent leaderboard
- full menu system and settings

The goal is to create a more complete arcade racing experience with progression and replay value.

---

## ⚙️ Technologies

- Python 3
- Pygame
- JSON (settings & leaderboard storage)

---

## 🧱 Base Features (from Practice 10–11)

- Player car movement (lane-based control)
- Scrolling road system
- Coin spawning on road
- Coin counter display
- Weighted coins with different values
- Increasing enemy speed after collecting coins

---

## 🚗 Gameplay Features

### 🛣 Lane Hazards & Road Events
- Oil spills (slows player)
- Barriers (block lanes)
- Potholes (temporary speed reduction)
- Speed boost strips (increase speed temporarily)

---

### 🚦 Dynamic Traffic System
- Enemy cars spawn randomly in lanes
- Collisions end the run (unless shield is active)
- Traffic density increases over time
- Safe spawn system (no overlapping with player)

---

## ⚡ Power-Ups System

| Power-up | Effect | Duration |
|----------|--------|----------|
| Nitro | Temporary speed boost | 3–5 seconds |
| Shield | Blocks one collision | Until hit |
| Repair | Restores crash / clears obstacle | Instant |

Rules:
- Only one power-up active at a time
- Power-ups disappear if not collected
- Active power-up shown on screen with timer

---

## 📊 Score & Progression

Score is calculated from:
- Coins collected
- Distance traveled
- Power-up bonuses

Additional features:
- Distance meter
- Progress tracking to finish line
- Increasing difficulty over time

---

## 🏆 Leaderboard System

- Saves top scores to `leaderboard.json`
- Stores:
  - player name
  - score
  - distance
- Displays **Top 10 players**
- Sorted automatically by highest score

---

## 👤 Username System

- Player enters name before starting game
- Name is used in leaderboard records

---

## 🧾 Game Screens

### 🏠 Main Menu
- Play
- Leaderboard
- Settings
- Quit

---

### ⚙️ Settings
- Sound ON/OFF
- Car color selection
- Difficulty level (Easy / Medium / Hard)
- Settings saved in `settings.json`

---

### 💀 Game Over Screen
- Final score
- Distance
- Coins collected
- Buttons:
  - Retry
  - Main Menu

---

### 🏆 Leaderboard Screen
- Top 10 scores
- Rank, name, score, distance
- Back button

---

## 💾 Data Persistence

### settings.json
Stores:
- sound setting
- car color
- difficulty

### leaderboard.json
Stores:
- player name
- score
- distance

---

## 📁 Project Structure
TSIS3/
├── main.py
├── racer.py
├── ui.py
├── persistence.py
├── settings.json
├── leaderboard.json
└── assets/
├── images/
└── sounds/


---

## 🚀 How to Run

```bash
pip install pygame
python main.py