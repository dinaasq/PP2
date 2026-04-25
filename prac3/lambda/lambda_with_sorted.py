# ============================================================
# lambda_with_sorted.py — Лямбда + sorted() и sort()
# ============================================================
# sorted(iterable, key=..., reverse=False) — возвращает новый отсортированный список
# list.sort(key=..., reverse=False)        — сортирует список на месте (in-place)

# 1. Сортировка по абсолютному значению
numbers = [-10, 3, -1, 7, -5, 2]
sorted_abs = sorted(numbers, key=lambda x: abs(x))
print(f"По абсолютному значению: {sorted_abs}")
# [-1, 2, 3, -5, 7, -10]


# 2. Сортировка строк по длине
fruits = ["банан", "яблоко", "киви", "арбуз", "слива"]
sorted_by_len = sorted(fruits, key=lambda f: len(f))
print(f"По длине строки: {sorted_by_len}")
# ['киви', 'банан', 'арбуз', 'слива', 'яблоко']


# 3. Сортировка строк по длине (обратный порядок)
sorted_by_len_desc = sorted(fruits, key=lambda f: len(f), reverse=True)
print(f"По длине (убывание): {sorted_by_len_desc}")
# ['яблоко', 'банан', 'арбуз', 'слива', 'киви']


# 4. Сортировка словарей по полю
students = [
    {"name": "Нұрлан",  "grade": 78},
    {"name": "Айгерим", "grade": 92},
    {"name": "Данияр",  "grade": 65},
    {"name": "Мария",   "grade": 88},
]

# По оценке (возрастание)
by_grade = sorted(students, key=lambda s: s["grade"])
print("\nПо оценке (возрастание):")
for s in by_grade:
    print(f"  {s['name']}: {s['grade']}")

# По имени (алфавит)
by_name = sorted(students, key=lambda s: s["name"])
print("\nПо имени (алфавит):")
for s in by_name:
    print(f"  {s['name']}: {s['grade']}")


# 5. Сортировка кортежей по второму элементу
pairs = [(1, "банан"), (3, "яблоко"), (2, "киви"), (4, "абрикос")]
sorted_pairs = sorted(pairs, key=lambda p: p[1])  # по строке
print(f"\nПо второму элементу: {sorted_pairs}")
# [(4, 'абрикос'), (1, 'банан'), (3, 'яблоко'), (2, 'киви')]  — алфавит


# 6. Многоуровневая сортировка — сначала по одному, потом по другому полю
employees = [
    {"name": "Анна",   "dept": "IT",  "salary": 90000},
    {"name": "Боб",    "dept": "HR",  "salary": 60000},
    {"name": "Карина", "dept": "IT",  "salary": 75000},
    {"name": "Дмитрий","dept": "HR",  "salary": 65000},
    {"name": "Елена",  "dept": "IT",  "salary": 90000},
]

# Сначала по отделу, потом по зарплате (убывание)
multi_sorted = sorted(employees,
                      key=lambda e: (e["dept"], -e["salary"]))
print("\nПо отделу, затем по зарплате (↓):")
for e in multi_sorted:
    print(f"  {e['dept']:4} | {e['salary']:6} | {e['name']}")


# 7. list.sort() — сортировка на месте
nums = [5, 1, 9, 3, 7, 2]
nums.sort(key=lambda x: x % 3)  # сортировка по остатку от деления на 3
print(f"\nSort на месте (по x%3): {nums}")


# 8. sorted() с объектами-классами
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def __repr__(self):
        return f"Product({self.name}, {self.price}₸)"

products = [
    Product("Ноутбук", 350000),
    Product("Мышь", 5000),
    Product("Монитор", 120000),
    Product("Клавиатура", 15000),
]

cheap_to_expensive = sorted(products, key=lambda p: p.price)
print("\nТовары по цене (дешевле → дороже):")
for p in cheap_to_expensive:
    print(f"  {p}")