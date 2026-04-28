import math
import tkinter as tk


current_color = "black"   # выбранный цвет
current_tool = "pencil"   # выбранный инструмент
brush_size = 3            # размер кисти


start_x = 0
start_y = 0
preview_id = None


def set_color(color):
    global current_color
    current_color = color


def set_tool(tool):
    global current_tool
    current_tool = tool


def set_size(size):
    global brush_size
    brush_size = size


def clear_canvas():
    canvas.delete("all")


# рисование фигур
def draw_shape(x1, y1, x2, y2):

    color = current_color
    width = brush_size

    if current_tool == "line":
        return canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

    if current_tool == "rectangle":
        return canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=width)

    if current_tool == "oval":
        return canvas.create_oval(x1, y1, x2, y2, outline=color, width=width)

    if current_tool == "square":
        # квадрат: с
        dx = x2 - x1
        dy = y2 - y1
        side = max(abs(dx), abs(dy))
        if dx < 0:
            sx = -side
        else:
            sx = side
        if dy < 0:
            sy = -side
        else:
            sy = side
        return canvas.create_rectangle(x1, y1, x1 + sx, y1 + sy,
                                       outline=color, width=width)

    if current_tool == "right_triangle":
        
        return canvas.create_polygon(x1, y1, x2, y1, x1, y2,
                                     outline=color, fill="", width=width)

    if current_tool == "eq_triangle":
        # равносторонний треугольник: 
        dx = x2 - x1
        dy = y2 - y1
        base = math.sqrt(dx * dx + dy * dy)
        if base < 1:
            return canvas.create_oval(x1, y1, x1 + 1, y1 + 1,
                                      outline=color, width=width)
        # середина основания
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        # перпендикуляр к основанию (единичный)
        px = -dy / base
        py = dx / base
        # высота равностороннего треугольника
        h = base * math.sqrt(3) / 2
        ax = mx + px * h
        ay = my + py * h
        return canvas.create_polygon(x1, y1, x2, y2, ax, ay,
                                     outline=color, fill="", width=width)

    if current_tool == "rhombus":
        # ромб
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        return canvas.create_polygon(mx, y1, x2, my, mx, y2, x1, my,
                                     outline=color, fill="", width=width)


# обработчики мыши
def on_press(event):
    global start_x, start_y, preview_id
    start_x = event.x
    start_y = event.y
    preview_id = None
    # карандаш и ластик — ставят точку сразу
    if current_tool == "pencil":
        canvas.create_line(event.x, event.y, event.x, event.y,
                           fill=current_color, width=brush_size)
    elif current_tool == "eraser":
        canvas.create_line(event.x, event.y, event.x, event.y,
                           fill="white", width=brush_size * 3)


def on_drag(event):
    global start_x, start_y, preview_id

    if current_tool == "pencil":
        canvas.create_line(start_x, start_y, event.x, event.y,
                           fill=current_color, width=brush_size)
        start_x = event.x
        start_y = event.y

    elif current_tool == "eraser":
        canvas.create_line(start_x, start_y, event.x, event.y,
                           fill="white", width=brush_size * 3)
        start_x = event.x
        start_y = event.y

    else:
        # фигуры: каждый раз стираем превью и рисуем заново
        if preview_id is not None:
            canvas.delete(preview_id)
        preview_id = draw_shape(start_x, start_y, event.x, event.y)


def on_release(event):
    global preview_id
    preview_id = None


#интерфейс
root = tk.Tk()
root.title("Paint - Practice 11")

# верхняя панель с инструментами
top = tk.Frame(root)
top.pack(side="top", fill="x")

tools = [
    ("Карандаш",      "pencil"),
    ("Ластик",        "eraser"),
    ("Линия",         "line"),
    ("Прямоугольник", "rectangle"),
    ("Овал",          "oval"),
    ("Квадрат",       "square"),
    ("Прям. треуг.",  "right_triangle"),
    ("Равн. треуг.",  "eq_triangle"),
    ("Ромб",          "rhombus"),
]
for text, tool_name in tools:
    tk.Button(top, text=text,
              command=lambda t=tool_name: set_tool(t)).pack(side="left", padx=2, pady=2)

tk.Button(top, text="Очистить", command=clear_canvas).pack(side="right", padx=4)

# панель с цветами и размерами
bottom = tk.Frame(root)
bottom.pack(side="top", fill="x")

colors = ["black", "red", "yellow", "green", "blue"]
for c in colors:
    tk.Button(bottom, bg=c, width=4,
              command=lambda col=c: set_color(col)).pack(side="left", padx=2, pady=2)

tk.Label(bottom, text="  Размер:").pack(side="left")
sizes = [("Маленький", 2), ("Средний", 5), ("Большой", 10)]
for label, value in sizes:
    tk.Button(bottom, text=label,
              command=lambda v=value: set_size(v)).pack(side="left", padx=2)

# холст
canvas = tk.Canvas(root, bg="white", width=800, height=500)
canvas.pack(fill="both", expand=True)

# подключаем мышь
canvas.bind("<ButtonPress-1>", on_press)
canvas.bind("<B1-Motion>", on_drag)
canvas.bind("<ButtonRelease-1>", on_release)

root.mainloop()