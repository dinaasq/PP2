# ============================================================
# lambda_with_filter.py — Лямбда + filter()
# ============================================================
# filter(function, iterable) — оставляет только те элементы,
# для которых функция возвращает True

# 1. Фильтрация чётных чисел
numbers = list(range(1, 21))
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(f"Чётные: {evens}")
# [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]


# 2. Фильтрация положительных чисел
mixed = [-5, 3, -1, 8, 0, -2, 7, 4, -9]
positive = list(filter(lambda x: x > 0, mixed))
print(f"Положительные: {positive}")  # [3, 8, 7, 4]


# 3. Фильтрация строк по длине
words = ["кот", "Python", "я", "программирование", "код", "алгоритм"]
long_words = list(filter(lambda w: len(w) > 4, words))
print(f"Длинные слова (>4 символов): {long_words}")
# ['Python', 'программирование', 'алгоритм']


# 4. Фильтрация словарей — студенты с оценкой >= 80
students = [
    {"name": "Айгерим", "grade": 92},
    {"name": "Нұрлан",  "grade": 65},
    {"name": "Мария",   "grade": 80},
    {"name": "Данияр",  "grade": 55},
    {"name": "Алина",   "grade": 88},
]
passed = list(filter(lambda s: s["grade"] >= 80, students))
print("\nСтуденты, сдавшие экзамен (>=80):")
for s in passed:
    print(f"  {s['name']}: {s['grade']}")


# 5. Фильтрация строк — только те, что начинаются с заглавной буквы
names = ["alice", "Bob", "charlie", "Diana", "eve", "Frank"]
capitalized = list(filter(lambda n: n[0].isupper(), names))
print(f"\nС заглавной буквы: {capitalized}")  # ['Bob', 'Diana', 'Frank']


# 6. Убираем None и пустые значения из списка
raw_data = [1, None, 3, "", 5, None, 7, 0, False, "данные"]
clean_data = list(filter(lambda x: x is not None and x != "", raw_data))
print(f"\nПосле очистки None и '': {clean_data}")
# [1, 3, 5, 7, 0, False, 'данные']

# Или через bool (убираем все falsy-значения)
truthy_data = list(filter(bool, raw_data))
print(f"Только truthy значения: {truthy_data}")
# [1, 3, 5, 7, 'данные']


# 7. filter + map вместе — конвейер обработки
#    Берём числа, оставляем нечётные, возводим в квадрат
pipeline_input = range(1, 11)
result = list(map(lambda x: x ** 2,
               filter(lambda x: x % 2 != 0, pipeline_input)))
print(f"\nНечётные числа в квадрате: {result}")
# [1, 9, 25, 49, 81]


# 8. Сравнение filter + lambda vs list comprehension
numbers = range(1, 16)

# Способ 1: filter + lambda
divisible_by_3 = list(filter(lambda x: x % 3 == 0, numbers))

# Способ 2: list comprehension
divisible_by_3_comp = [x for x in numbers if x % 3 == 0]

print(f"\nfilter: {divisible_by_3}")       # [3, 6, 9, 12, 15]
print(f"comp:   {divisible_by_3_comp}")    # [3, 6, 9, 12, 15]