# ============================================================
# args_kwargs.py — *args и **kwargs
# ============================================================

# 1. *args — произвольное количество позиционных аргументов
#    Внутри функции args — это кортеж (tuple)
def sum_all(*args):
    """Складывает любое количество чисел."""
    total = 0
    for number in args:
        total += number
    return total

print(sum_all(1, 2, 3))           # 6
print(sum_all(10, 20, 30, 40))    # 100
print(sum_all(5))                 # 5
print(sum_all())                  # 0


# 2. **kwargs — произвольное количество именованных аргументов
#    Внутри функции kwargs — это словарь (dict)
def print_profile(**kwargs):
    """Выводит профиль пользователя из именованных аргументов."""
    print("\n--- Профиль ---")
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

print_profile(name="Айгерим", age=25, city="Алматы", job="разработчик")
print_profile(brand="Tesla", model="Model 3", year=2023)


# 3. Комбинация: обычные параметры + *args + **kwargs
def full_function(required_param, *args, keyword_only="default", **kwargs):
    """
    Демонстрирует все виды параметров вместе.
    Порядок: обычные → *args → keyword_only → **kwargs
    """
    print(f"\nОбязательный: {required_param}")
    print(f"*args: {args}")
    print(f"keyword_only: {keyword_only}")
    print(f"**kwargs: {kwargs}")

full_function(
    "первый",            # required_param
    "второй", "третий",  # args
    keyword_only="особый",
    color="синий", size="XL"  # kwargs
)


# 4. Распаковка списка в *args при вызове функции
def add_three(a, b, c):
    return a + b + c

numbers = [10, 20, 30]
result = add_three(*numbers)   # распаковка списка
print(f"\n*распаковка: {result}")  # 60

coords = (1, 2, 3)
print(add_three(*coords))  # 6


# 5. Распаковка словаря в **kwargs при вызове функции
def greet(name, greeting, punctuation):
    print(f"{greeting}, {name}{punctuation}")

params = {"name": "Мира", "greeting": "Добрый день", "punctuation": "!"}
greet(**params)  # Добрый день, Мира!


# 6. Практический пример: универсальный логгер
def log(level, *messages, separator=" | ", **context):
    """
    Универсальная функция логирования.
    level    — уровень (INFO, WARNING, ERROR)
    messages — одно или несколько сообщений
    separator — разделитель между сообщениями
    context  — дополнительные данные (user_id, ip, и т.д.)
    """
    combined = separator.join(str(m) for m in messages)
    ctx_str = " ".join(f"{k}={v}" for k, v in context.items())
    print(f"[{level}] {combined}" + (f" ({ctx_str})" if ctx_str else ""))

log("INFO", "Пользователь вошёл")
log("WARNING", "Неверный пароль", "Попытка 2/3", user_id=42, ip="192.168.1.1")
log("ERROR", "База данных недоступна", separator=" >> ", service="db", port=5432)


# 7. Передача *args и **kwargs дальше (forwarding)
def wrapper(*args, **kwargs):
    """Оборачивает вызов sum_all, добавляя логику до/после."""
    print(f"Вызываю sum_all с args={args}")
    result = sum_all(*args)
    print(f"Результат: {result}")
    return result

wrapper(1, 2, 3, 4, 5)