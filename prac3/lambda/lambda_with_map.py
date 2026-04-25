# ============================================================
# lambda_with_map.py — Лямбда + map()
# ============================================================
# map(function, iterable) — применяет функцию к каждому элементу
# Возвращает map-объект → конвертируем в list()

# 1. Квадрат каждого числа
numbers = [1, 2, 3, 4, 5, 6]
squares = list(map(lambda x: x ** 2, numbers))
print(f"Квадраты: {squares}")
# [1, 4, 9, 16, 25, 36]


# 2. Перевод Цельсий → Фаренгейт
celsius = [0, 20, 37, 100]
fahrenheit = list(map(lambda c: (c * 9/5) + 32, celsius))
print(f"Фаренгейт: {fahrenheit}")
# [32.0, 68.0, 98.6, 212.0]


# 3. Перевод строк в верхний регистр
words = ["python", "lambda", "функция", "программа"]
upper_words = list(map(lambda w: w.upper(), words))
print(f"Верхний регистр: {upper_words}")
# ['PYTHON', 'LAMBDA', 'ФУНКЦИЯ', 'ПРОГРАММА']


# 4. map с двумя итерируемыми объектами
#    Лямбда принимает по одному элементу из каждого
prices = [100, 250, 75, 400]
discounts = [0.1, 0.2, 0.05, 0.15]  # скидки в долях

final_prices = list(map(lambda p, d: round(p * (1 - d), 2), prices, discounts))
print(f"Цены со скидкой: {final_prices}")
# [90.0, 200.0, 71.25, 340.0]


# 5. Форматирование данных — добавляем единицы измерения
distances_km = [1.5, 3.2, 10.0, 0.8]
formatted = list(map(lambda d: f"{d} км", distances_km))
print(f"Расстояния: {formatted}")
# ['1.5 км', '3.2 км', '10.0 км', '0.8 км']


# 6. map для обработки словарей (извлечение поля)
students = [
    {"name": "Айгерим", "grade": 92},
    {"name": "Нұрлан", "grade": 78},
    {"name": "Мария", "grade": 85},
]
names = list(map(lambda s: s["name"], students))
grades = list(map(lambda s: s["grade"], students))
print(f"Студенты: {names}")   # ['Айгерим', 'Нұрлан', 'Мария']
print(f"Оценки: {grades}")    # [92, 78, 85]


# 7. Вложенный map — применяем к матрице
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
doubled_matrix = list(map(lambda row: list(map(lambda x: x * 2, row)), matrix))
print(f"Удвоенная матрица:")
for row in doubled_matrix:
    print(f"  {row}")
# [2, 4, 6]
# [8, 10, 12]
# [14, 16, 18]


# 8. Сравнение map + lambda vs list comprehension
nums = range(1, 8)

# Способ 1: map + lambda
cubes_map = list(map(lambda x: x ** 3, nums))

# Способ 2: list comprehension (часто предпочтительнее по читаемости)
cubes_comp = [x ** 3 for x in nums]

print(f"map:   {cubes_map}")   # [1, 8, 27, 64, 125, 216, 343]
print(f"comp:  {cubes_comp}")  # [1, 8, 27, 64, 125, 216, 343]
print(f"Равны: {cubes_map == cubes_comp}")  # True