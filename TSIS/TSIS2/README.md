# 🎨 TSIS 2: Paint Application — Extended Drawing Tools

## 📌 Description

This project is an extended **Paint application built with Pygame**.  
It enhances previous versions by adding freehand drawing, shape tools, brush control, text input, flood fill, and canvas saving functionality.

The goal is to simulate a simple digital drawing editor using only built-in Pygame features.

---

## ⚙️ Technologies

- Python 3
- Pygame
- datetime (for file naming)

---

## 🧱 Base Features (from Practice 10–11)

- Rectangle tool
- Circle tool
- Eraser
- Color picker
- Square tool
- Right triangle
- Equilateral triangle
- Rhombus

---

## ✏️ New Features

### 🖊 Pencil Tool (Freehand Drawing)
- Draw continuously while holding mouse button
- Uses smooth line interpolation between cursor positions

---

### 📏 Straight Line Tool
- Click to set start point
- Drag mouse to preview line
- Release to draw final line

---

### 📐 Brush Size Control
Three brush sizes:
- Small → 2 px
- Medium → 5 px
- Large → 10 px

Controls:
- `1` → small
- `2` → medium
- `3` → large

Applies to:
- pencil
- line
- all shapes (rectangle, circle, triangles, etc.)

---

### 🪣 Flood Fill Tool
- Click inside a closed area to fill it with selected color
- Implemented using pixel-based scanning (`get_at`, `set_at`)
- Works like a simple paint bucket tool

---

### 💾 Save Canvas
- Press **Ctrl + S**
- Saves canvas as `.png`
- Uses timestamp to avoid overwriting files

Example:

---

### ✍️ Text Tool
- Click to place text cursor
- Type text directly on canvas
- `Enter` → confirm and draw text
- `Escape` → cancel input
- Uses `pygame.font`

---

## 🧠 Controls Summary

| Action | Control |
|--------|--------|
| Pencil tool | Mouse drag |
| Line tool | Click + drag |
| Brush size small | 1 |
| Brush size medium | 2 |
| Brush size large | 3 |
| Save canvas | Ctrl + S |
| Text input | Click + type |
| Confirm text | Enter |
| Cancel text | Escape |

---

## 📁 Project Structure
TSIS2/
├── paint.py
├── tools.py
└── assets/
└── icons / fonts (optional)


---

## 🚀 How to Run

```bash
pip install pygame
python paint.py