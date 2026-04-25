# ============================================================
# multiple_inheritance.py — Множественное наследование
# ============================================================
# Python позволяет классу наследовать от нескольких родителей:
#   class Child(Parent1, Parent2, Parent3):
# MRO (Method Resolution Order) — порядок поиска методов,
# определяется алгоритмом C3-линеаризации.

# ── 1. Простое множественное наследование ────────────────────
class Flyable:
    """Миксин: умеет летать."""
    def fly(self):
        print(f"{type(self).__name__} летит! ✈")

    def altitude(self):
        return "Высота: 1000 м"


class Swimmable:
    """Миксин: умеет плавать."""
    def swim(self):
        print(f"{type(self).__name__} плывёт! 🏊")

    def depth(self):
        return "Глубина: 10 м"


class Walkable:
    """Миксин: умеет ходить."""
    def walk(self):
        print(f"{type(self).__name__} идёт пешком. 🚶")


class Duck(Flyable, Swimmable, Walkable):
    """Утка умеет летать, плавать и ходить."""
    def quack(self):
        print("Кря-кря!")


donald = Duck()
donald.fly()    # Duck летит!
donald.swim()   # Duck плывёт!
donald.walk()   # Duck идёт пешком.
donald.quack()  # Кря-кря!
print(donald.altitude())  # Высота: 1000 м


# ── 2. MRO — порядок поиска методов ─────────────────────────
print("\n--- MRO Duck ---")
print(Duck.__mro__)
# (<class 'Duck'>, <class 'Flyable'>, <class 'Swimmable'>, <class 'Walkable'>, <class 'object'>)


# ── 3. Конфликт имён — MRO решает, чей метод победит ────────
class A:
    def hello(self):
        return "Hello from A"

class B(A):
    def hello(self):
        return "Hello from B"

class C(A):
    def hello(self):
        return "Hello from C"

class D(B, C):
    pass   # не переопределяет hello()

d = D()
print(f"\nD().hello() → {d.hello()}")  # Hello from B (B идёт раньше C в MRO)
print(D.__mro__)
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)


# ── 4. Паттерн Mixin — функциональные примеси ────────────────
class JSONMixin:
    """Миксин: добавляет метод to_json() любому классу."""
    def to_json(self):
        import json
        return json.dumps(self.__dict__, ensure_ascii=False, indent=2)


class LogMixin:
    """Миксин: добавляет логирование методов."""
    def log(self, message):
        print(f"[{type(self).__name__}] {message}")


class TimestampMixin:
    """Миксин: добавляет временну́ю метку создания."""
    def __init__(self, *args, **kwargs):
        import datetime
        super().__init__(*args, **kwargs)
        self.created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class User(TimestampMixin, JSONMixin, LogMixin):
    def __init__(self, name, email):
        super().__init__()   # TimestampMixin.__init__ → object.__init__
        self.name = name
        self.email = email

    def greet(self):
        self.log(f"Приветствую пользователя {self.name}")
        return f"Привет, {self.name}!"


user = User("Айгерим", "aigerim@example.com")
user.greet()             # [User] Приветствую пользователя Айгерим
print(user.to_json())    # JSON представление объекта
print(f"Создан: {user.created_at}")


# ── 5. super() с множественным наследованием (cooperative) ───
class Base:
    def action(self):
        print("Base.action")

class Mixin1(Base):
    def action(self):
        print("Mixin1.action — до Base")
        super().action()
        print("Mixin1.action — после Base")

class Mixin2(Base):
    def action(self):
        print("Mixin2.action — до Base")
        super().action()
        print("Mixin2.action — после Base")

class Combined(Mixin1, Mixin2):
    def action(self):
        print("Combined.action — начало")
        super().action()
        print("Combined.action — конец")

print("\n--- Кооперативное super() ---")
c = Combined()
c.action()
# Combined.action — начало
# Mixin1.action — до Base
# Mixin2.action — до Base
# Base.action
# Mixin2.action — после Base
# Mixin1.action — после Base
# Combined.action — конец