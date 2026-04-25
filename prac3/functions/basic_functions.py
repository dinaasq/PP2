# ============================================================
# basic_functions.py — Базовые функции в Python
# ============================================================

# 1. Простая функция без параметров
def greet():
    """Выводит приветственное сообщение."""
    print("Привет, мир!")

greet()  # Привет, мир!


# 2. Функция с одним параметром
def greet_user(name):
    """Приветствует конкретного пользователя."""
    print(f"Привет, {name}!")

greet_user("Алиса")   # Привет, Алиса!
greet_user("Боб")     # Привет, Боб!


# 3. Функция с несколькими параметрами
def add(a, b):
    """Складывает два числа и возвращает результат."""
    return a + b

result = add(3, 5)
print(f"3 + 5 = {result}")  # 3 + 5 = 8


# 4. Функция с параметром по умолчанию
def power(base, exponent=2):
    """Возводит base в степень exponent (по умолчанию квадрат)."""
    return base ** exponent

print(power(4))       # 16  (4^2)
print(power(2, 10))   # 1024 (2^10)


# 5. Функция, которая ничего не возвращает (возвращает None)
def print_divider(symbol="-", length=30):
    """Печатает разделительную линию."""
    print(symbol * length)

print_divider()          # ------------------------------
print_divider("=", 20)   # ====================


# 6. Вложенная функция (inner function)
def outer():
    """Внешняя функция содержит внутреннюю."""
    def inner():
        print("Я внутренняя функция!")
    print("Я внешняя функция!")
    inner()

outer()
# Я внешняя функция!
# Я внутренняя функция!


# 7. Рекурсивная функция — факториал
def factorial(n):
    """Вычисляет n! рекурсивно."""
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(f"5! = {factorial(5)}")   # 120
print(f"10! = {factorial(10)}") # 3628800


# 8. Функция с документацией (docstring)
def circle_area(radius):
    """
    Вычисляет площадь круга.

    Args:
        radius (float): Радиус круга.

    Returns:
        float: Площадь круга.
    """
    import math
    return math.pi * radius ** 2

area = circle_area(5)
print(f"Площадь круга с радиусом 5: {area:.2f}")  # 78.54
print(circle_area.__doc__)  # Вывод документации функции