# ============================================================
# function_arguments.py — Виды аргументов функций
# ============================================================

# 1. Позиционные аргументы (Positional Arguments)
#    Передаются строго по порядку
def describe_pet(animal_type, pet_name):
    print(f"У меня есть {animal_type} по имени {pet_name}.")

describe_pet("кот", "Мурзик")      # У меня есть кот по имени Мурзик.
describe_pet("собака", "Шарик")    # У меня есть собака по имени Шарик.


# 2. Именованные аргументы (Keyword Arguments)
#    Порядок не важен — указываем имя параметра явно
def make_shirt(size, text):
    print(f"Футболка размера {size} с надписью '{text}'.")

make_shirt(size="L", text="Python разработчик")
make_shirt(text="Hello World", size="M")  # порядок изменён — всё равно работает


# 3. Аргументы по умолчанию (Default Values)
#    Если аргумент не передан — используется значение по умолчанию
def greet(name, language="ru"):
    messages = {
        "ru": f"Привет, {name}!",
        "en": f"Hello, {name}!",
        "kz": f"Сәлем, {name}!",
    }
    print(messages.get(language, f"Hi, {name}!"))

greet("Айгерим")            # Привет, Айгерим!
greet("Alice", "en")        # Hello, Alice!
greet("Нұрлан", "kz")       # Сәлем, Нұрлан!


# 4. Обязательные vs необязательные параметры
#    Параметры без дефолта — обязательные; с дефолтом — необязательные
def create_user(username, email, is_admin=False, age=None):
    print(f"Пользователь: {username}, Email: {email}, "
          f"Админ: {is_admin}, Возраст: {age}")

create_user("john_doe", "john@example.com")
create_user("admin_user", "admin@site.com", is_admin=True, age=30)


# 5. Передача изменяемых объектов (список) — мутация внутри функции
def append_greeting(name, greetings_list):
    """Добавляет приветствие в список — изменяет оригинальный список!"""
    greetings_list.append(f"Привет, {name}!")

messages = []
append_greeting("Мария", messages)
append_greeting("Иван", messages)
print(messages)  # ['Привет, Мария!', 'Привет, Иван!']


# 6. Передача неизменяемых объектов (int) — оригинал НЕ меняется
def try_to_double(number):
    number = number * 2   # создаётся локальная копия
    print(f"Внутри функции: {number}")

x = 10
try_to_double(x)
print(f"Снаружи функции: {x}")  # x всё ещё 10


# 7. Смешанный вызов: позиционные + именованные
def order_pizza(size, crust, *toppings_list, delivery=False):
    print(f"\nЗаказ пиццы:")
    print(f"  Размер: {size}, Тесто: {crust}")
    print(f"  Топпинги: {', '.join(toppings_list) if toppings_list else 'нет'}")
    print(f"  Доставка: {'да' if delivery else 'нет'}")

order_pizza("большая", "тонкое", "сыр", "грибы", "перец", delivery=True)
order_pizza("маленькая", "толстое")