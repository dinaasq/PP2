# ============================================================
# return_values.py — Возвращаемые значения функций
# ============================================================

# 1. Возврат простого значения
def square(n):
    """Возвращает квадрат числа."""
    return n ** 2

print(square(7))   # 49
print(square(12))  # 144


# 2. Возврат нескольких значений (кортеж)
def min_max(numbers):
    """Возвращает минимум и максимум списка."""
    return min(numbers), max(numbers)

data = [4, 1, 9, 2, 7, 5]
minimum, maximum = min_max(data)
print(f"Мин: {minimum}, Макс: {maximum}")  # Мин: 1, Макс: 9

# Можно получить как кортеж целиком
result = min_max(data)
print(type(result), result)  # <class 'tuple'> (1, 9)


# 3. Возврат словаря (удобно для структурированных данных)
def get_user_info(name, age, city):
    """Возвращает информацию о пользователе в виде словаря."""
    return {
        "name": name,
        "age": age,
        "city": city,
        "is_adult": age >= 18
    }

user = get_user_info("Данияр", 22, "Алматы")
print(user)
print(f"Совершеннолетний: {user['is_adult']}")  # True


# 4. Возврат списка (генерация последовательности)
def fibonacci(n):
    """Возвращает список из первых n чисел Фибоначчи."""
    sequence = [0, 1]
    for _ in range(n - 2):
        sequence.append(sequence[-1] + sequence[-2])
    return sequence[:n]

print(fibonacci(10))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# 5. Ранний возврат (early return) — выход из функции досрочно
def divide(a, b):
    """Делит a на b. Возвращает None при делении на ноль."""
    if b == 0:
        print("Ошибка: деление на ноль!")
        return None   # ранний выход
    return a / b

print(divide(10, 2))   # 5.0
print(divide(7, 0))    # Ошибка: деление на ноль! → None


# 6. Функция возвращает другую функцию (замыкание / closure)
def make_multiplier(factor):
    """Создаёт функцию-умножитель на заданный factor."""
    def multiplier(number):
        return number * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
print(double(triple(4)))  # double(12) = 24


# 7. Возврат булевого значения (предикат-функция)
def is_palindrome(text):
    """Проверяет, является ли строка палиндромом."""
    cleaned = text.lower().replace(" ", "")
    return cleaned == cleaned[::-1]

print(is_palindrome("racecar"))    # True
print(is_palindrome("level"))      # True
print(is_palindrome("hello"))      # False
print(is_palindrome("A man a plan a canal Panama".replace(" ","")))  # True


# 8. Использование возвращаемого значения в цепочке вызовов
def add(a, b): return a + b
def multiply(a, b): return a * b
def subtract(a, b): return a - b

# Вычисляем: (3 + 4) * 2 - 1
answer = subtract(multiply(add(3, 4), 2), 1)
print(f"(3 + 4) * 2 - 1 = {answer}")  # 13