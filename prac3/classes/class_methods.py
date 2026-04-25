# ============================================================
# class_methods.py — Методы экземпляра, класса и статические
# ============================================================

# ── 1. Методы экземпляра (instance methods) ─────────────────
#    Первый параметр — self (текущий объект)
class Circle:
    PI = 3.14159265358979  # атрибут класса (константа)

    def __init__(self, radius):
        self.radius = radius   # атрибут экземпляра

    # Метод экземпляра — работает с self
    def area(self):
        return Circle.PI * self.radius ** 2

    def circumference(self):
        return 2 * Circle.PI * self.radius

    def scale(self, factor):
        """Масштабирует круг, изменяя радиус."""
        self.radius *= factor

    def __str__(self):
        return f"Circle(radius={self.radius:.2f})"

c = Circle(5)
print(f"Площадь: {c.area():.2f}")          # 78.54
print(f"Длина окружности: {c.circumference():.2f}")  # 31.42
c.scale(2)
print(c)   # Circle(radius=10.00)


# ── 2. @classmethod — метод класса ──────────────────────────
#    Первый параметр — cls (сам класс, а не экземпляр)
#    Часто используется как альтернативный конструктор
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_str):
        """Создаёт объект Date из строки формата 'YYYY-MM-DD'."""
        year, month, day = map(int, date_str.split("-"))
        return cls(year, month, day)

    @classmethod
    def today(cls):
        """Создаёт объект Date с сегодняшней датой."""
        import datetime
        d = datetime.date.today()
        return cls(d.year, d.month, d.day)

    def __str__(self):
        return f"{self.day:02d}.{self.month:02d}.{self.year}"

d1 = Date(2024, 3, 15)
d2 = Date.from_string("2024-07-20")
d3 = Date.today()

print(f"\nd1: {d1}")   # 15.03.2024
print(f"d2: {d2}")    # 20.07.2024
print(f"Сегодня: {d3}")


# ── 3. @staticmethod — статический метод ────────────────────
#    Не получает ни self, ни cls
#    Логически связан с классом, но не зависит от состояния объекта
class MathUtils:
    @staticmethod
    def is_prime(n):
        """Проверяет, является ли n простым числом."""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def gcd(a, b):
        """Наибольший общий делитель (алгоритм Евклида)."""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def celsius_to_fahrenheit(c):
        return c * 9/5 + 32

# Статические методы можно вызывать без создания объекта
print(f"\n7 простое? {MathUtils.is_prime(7)}")   # True
print(f"9 простое? {MathUtils.is_prime(9)}")     # False
print(f"НОД(48,18) = {MathUtils.gcd(48, 18)}")  # 6
print(f"37°C = {MathUtils.celsius_to_fahrenheit(37)}°F")  # 98.6°F


# ── 4. Магические (dunder) методы ───────────────────────────
#    __repr__, __len__, __add__, __eq__, __lt__
class Vector:
    """Двумерный вектор с перегрузкой операторов."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        """Представление для разработчика (eval-пригодное)."""
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        """Читаемое представление."""
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        """Перегрузка оператора +"""
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        """Перегрузка умножения на скаляр"""
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        """Перегрузка =="""
        return self.x == other.x and self.y == other.y

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(f"\nv1 + v2 = {v1 + v2}")    # (4, 6)
print(f"v1 * 3  = {v1 * 3}")       # (3, 6)
print(f"|v2|    = {v2.magnitude():.2f}")  # 5.00
print(f"v1 == v2: {v1 == v2}")     # False
print(f"repr: {repr(v1)}")          # Vector(1, 2)