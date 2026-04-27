import pygame
import tools
import os

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 1150, 750  # Окно чуть больше холста для панелей
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

# Холст (отдельная поверхность для рисования)
canvas = pygame.Surface((1000, 700))
canvas.fill((255, 255, 255))

# Состояние приложения
current_tool = 'pencil'
active_color = (0, 0, 0)
thickness = 2
drawing = False
start_pos = None

# Шрифт для текста
font = pygame.font.Font("assets/fonts.TTF", 20)
text_active = False
text_content = ""
text_pos = (0, 0)

# Список инструментов и загрузка иконок
TOOLS = [
    'pencil', 'eraser', 'line', 'rectangle', 'circle', 
    'square', 'right_triangle', 'equilateral_triangle', 
    'rhombus', 'fill', 'text'
]
icons = {}
buttons = {}

# Настройка палитры цветов
COLORS = {
    'red': (255, 0, 0),
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'black': (0, 0, 0),
    'green': (0, 255, 0)
}
color_buttons = {}

# Разместим цвета ниже инструментов
start_y_colors = 20 + len(TOOLS) * 40 + 20 
for i, (name, value) in enumerate(COLORS.items()):
    col = i % 3  # колонка (0, 1, 2)
    row = i // 3 # строка (0, 1)
    color_buttons[name] = (pygame.Rect(1025 + col * 35, start_y_colors + row * 35, 25, 25), value)
    
    
    
    
for i, tool in enumerate(TOOLS):
    path = f"assets/{tool}.png"
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        icons[tool] = pygame.transform.scale(img, (30, 30))
    else:
        # Заглушка, если иконка не найдена
        icons[tool] = pygame.Surface((30, 30))
        icons[tool].fill((100, 100, 100))
    # Размещаем кнопки в правой колонке
    buttons[tool] = pygame.Rect(1050, 20 + i * 40, 30, 30)

# Словарь для вызова функций отрисовки из tools.py
SHAPE_FUNCTIONS = {
    'rectangle': tools.draw_rect,
    'circle': tools.draw_circle,
    'square': tools.draw_square,
    'right_triangle': tools.draw_right_triangle,
    'equilateral_triangle': tools.draw_equilateral_triangle,
    'rhombus': tools.draw_rhombus
}

running = True
clock = pygame.time.Clock()

while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # ГОРЯЧИЕ КЛАВИШИ
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: thickness = 2
            if event.key == pygame.K_2: thickness = 5
            if event.key == pygame.K_3: thickness = 10
            
            # Сохранение Ctrl+S
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                filename = tools.get_timestamped_filename()
                pygame.image.save(canvas, filename)
                print(f"Canvas saved as {filename}")

            # Обработка ввода текста
            if text_active:
                if event.key == pygame.K_RETURN:
                    # Рисуем текст на холсте окончательно
                    txt_surf = font.render(text_content, True, active_color)
                    canvas.blit(txt_surf, text_pos)
                    text_active = False
                    text_content = ""
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text_content = text_content[:-1]
                else:
                    text_content += event.unicode

        # МЫШЬ
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверка нажатия на кнопки инструментов
            button_hit = False
            for tool_name, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    current_tool = tool_name
                    button_hit = True
                    break
            
            # Проверка клика по палитре цветов
            for name, (rect, val) in color_buttons.items():
                if rect.collidepoint(event.pos):
                    active_color = val # Устанавливаем кортеж цвета (R, G, B)
                    hit = True
                    break
            
            # Если нажали на холст
            if not button_hit and event.pos[0] < 1000 and event.pos[1] < 700:
                if current_tool == 'fill':
                    tools.flood_fill(canvas, event.pos[0], event.pos[1], active_color)
                elif current_tool == 'text':
                    text_active = True
                    text_pos = event.pos
                    text_content = ""
                else:
                    drawing = True
                    start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                # Окончательная отрисовка фигур на холст
                if current_tool == 'line':
                    pygame.draw.line(canvas, active_color, start_pos, event.pos, thickness)
                elif current_tool in SHAPE_FUNCTIONS:
                    SHAPE_FUNCTIONS[current_tool](canvas, start_pos, event.pos, thickness, active_color)
                drawing = False

    # Логика непрерывного рисования (Карандаш и Ластик)
    if drawing:
        if current_tool == 'pencil':
            pygame.draw.line(canvas, active_color, start_pos, mouse_pos, thickness)
            start_pos = mouse_pos
        elif current_tool == 'eraser':
            pygame.draw.line(canvas, (255, 255, 255),start_pos, mouse_pos, thickness * 10)
            start_pos = mouse_pos

    # --- СЕКЦИЯ ОТРИСОВКИ НА ЭКРАН ---
    screen.fill((45, 45, 45)) # Темный фон интерфейса
    screen.blit(canvas, (0, 0)) # Рисуем наш холст

    # Предпросмотр (Preview) фигур пока тянем мышь
    if drawing and start_pos:
        if current_tool == 'line':
            pygame.draw.line(screen, active_color, start_pos, mouse_pos, thickness)
        elif current_tool in SHAPE_FUNCTIONS:
            SHAPE_FUNCTIONS[current_tool](screen, start_pos, mouse_pos, thickness, active_color)

    # Рисование панели инструментов
    for tool_name, rect in buttons.items():
        # Подсветка выбранного инструмента
        bg_color = (80, 80, 180) if current_tool == tool_name else (60, 60, 60)
        pygame.draw.rect(screen, bg_color, rect.inflate(10, 10), 0, 5)
        pygame.draw.rect(screen, (200, 200, 200), rect.inflate(10, 10), 2, 5)
        screen.blit(icons[tool_name], rect.topleft)
    # Рисуем палитру цветов
    # Отрисовка палитры (кучкой)
    for name, (rect, val) in color_buttons.items():
        # Рисуем сам цветной квадрат
        # Мы используем 'val' для цвета и 'rect' для позиции
        pygame.draw.rect(screen, val, rect, 0, 3) 
        
        # Если этот цвет выбран, рисуем белую рамку вокруг
        if active_color == val:
            pygame.draw.rect(screen, (255, 255, 255), rect.inflate(6, 6), 2, 3)

    # Отображение текста в процессе ввода
    if text_active:
        preview_txt = font.render(text_content + "|", True, active_color)
        screen.blit(preview_txt, text_pos)

    # Информационная панель
    info_txt = f"Tool: {current_tool.upper()} | Size: {thickness} (1,2,3) | Ctrl+S to Save"
    screen.blit(font.render(info_txt, True, (255, 255, 255)), (10, 715))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()