# ============================================================
# lambda_basics.py — Основы лямбда-функций
# ============================================================
# Синтаксис: lambda аргументы : выражение
# Лямбда — анонимная однострочная функция

# 1. Простая лямбда — квадрат числа
square = lambda x: x ** 2
print(square(5))   # 25
print(square(9))   # 81

# Эквивалент обычной функции:
# def square(x): return x ** 2


# 2. Лямбда с двумя аргументами — сумма
add = lambda a, b: a + b
print(add(3, 7))    # 10
print(add(100, 200))  # 300


# 3. Лямбда с условием (тернарный оператор)
is_even = lambda n: "чётное" if n % 2 == 0 else "нечётное"
print(is_even(4))   # чётное
print(is_even(7))   # нечётное


# 4. Лямбда с тремя аргументами — объём прямоугольника
volume = lambda l, w, h: l * w * h
print(volume(3, 4, 5))   # 60


# 5. Немедленный вызов лямбды (IIFE — Immediately Invoked)
result = (lambda x, y: x * y)(6, 7)
print(f"6 * 7 = {result}")  # 42


# 6. Лямбда как аргумент другой функции
def apply(func, value):
    """Применяет функцию к значению."""
    return func(value)

print(apply(lambda x: x + 100, 5))    # 105
print(apply(lambda x: x.upper(), "hello"))  # HELLO


# 7. Список лямбда-функций
operations = [
    lambda x: x + 10,
    lambda x: x * 2,
    lambda x: x ** 2,
    lambda x: x - 5,
]

number = 4
for op in operations:
    print(op(number), end="  ")
# 14  8  16  -1
print()


# 8. Лямбда с несколькими условиями (цепочка elif через вложение)
classify = lambda n: "отрицательное" if n < 0 else ("ноль" if n == 0 else "положительное")
print(classify(-5))   # отрицательное
print(classify(0))    # ноль
print(classify(3))    # положительное


# 9. Когда НЕ стоит использовать лямбду
# Плохо — сложная логика в лямбде нечитаема:
# bad = lambda x: x**2 if x > 0 else (-x)**2 if x < 0 else 0

# Хорошо — для сложной логики используем обычную функцию:
def abs_square(x):
    """Квадрат абсолютного значения числа."""
    return abs(x) ** 2

print(abs_square(-3))  # 9
print(abs_square(4))   # 16