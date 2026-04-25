# ============================================================
# init_method.py — Метод __init__() и параметр self
# ============================================================
# __init__ вызывается автоматически при создании объекта.
# self — ссылка на текущий экземпляр класса (аналог "this" в Java/C#)

# 1. Базовый __init__ с обязательными параметрами
class Student:
    """Студент учебного заведения."""

    def __init__(self, name, age, major):
        # self.атрибут = значение — сохраняем данные внутри объекта
        self.name = name
        self.age = age
        self.major = major
        self.grades = []          # атрибут-список, общий для всех, но независимый

    def __str__(self):
        return f"Student({self.name}, {self.age}, {self.major})"

s1 = Student("Айгерим", 20, "CS")
s2 = Student("Нұрлан", 22, "Math")
print(s1)  # Student(Айгерим, 20, CS)
print(s2)  # Student(Нұрлан, 22, Math)


# 2. __init__ с параметрами по умолчанию
class BankAccount:
    """Банковский счёт."""

    def __init__(self, owner, balance=0.0, currency="KZT"):
        self.owner = owner
        self.balance = balance
        self.currency = currency
        self.transactions = []  # история операций

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"+{amount}")
        print(f"Пополнение {amount} {self.currency}. Баланс: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Недостаточно средств!")
            return
        self.balance -= amount
        self.transactions.append(f"-{amount}")
        print(f"Снятие {amount} {self.currency}. Баланс: {self.balance}")

    def __str__(self):
        return f"Счёт {self.owner}: {self.balance} {self.currency}"

account = BankAccount("Данияр")
account.deposit(50000)
account.deposit(20000)
account.withdraw(15000)
print(account)
print(f"История: {account.transactions}")


# 3. __init__ с вычисляемыми атрибутами
class Rectangle:
    """Прямоугольник с автовычислением площади и периметра."""

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Вычисляемые атрибуты инициализируются сразу
        self.area = width * height
        self.perimeter = 2 * (width + height)

    def resize(self, new_width, new_height):
        """Изменяет размеры и пересчитывает площадь."""
        self.width = new_width
        self.height = new_height
        self.area = new_width * new_height
        self.perimeter = 2 * (new_width + new_height)

    def __str__(self):
        return (f"Прямоугольник {self.width}×{self.height}: "
                f"площадь={self.area}, периметр={self.perimeter}")

rect = Rectangle(5, 3)
print(rect)       # Прямоугольник 5×3: площадь=15, периметр=16
rect.resize(10, 4)
print(rect)       # Прямоугольник 10×4: площадь=40, периметр=28


# 4. self — это ссылка на конкретный экземпляр
#    Каждый объект хранит свои данные отдельно
class Counter:
    def __init__(self, start=0):
        self.count = start  # у каждого Counter свой счётчик

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0

c1 = Counter()
c2 = Counter(100)

c1.increment()
c1.increment()
c2.increment()

print(f"c1.count = {c1.count}")  # 2 (независимо от c2)
print(f"c2.count = {c2.count}")  # 101


# 5. __init__ вызывает другие методы класса
class TemperatureSensor:
    """Датчик температуры с историей измерений."""

    def __init__(self, name, unit="C"):
        self.name = name
        self.unit = unit
        self.readings = []
        self._validate_unit()  # метод вызывается при создании

    def _validate_unit(self):
        """Проверяет единицу измерения (приватный метод)."""
        allowed = {"C", "F", "K"}
        if self.unit not in allowed:
            raise ValueError(f"Единица должна быть одной из {allowed}")

    def record(self, temp):
        self.readings.append(temp)

    def average(self):
        if not self.readings:
            return None
        return sum(self.readings) / len(self.readings)

sensor = TemperatureSensor("Кухня")
sensor.record(22.5)
sensor.record(23.1)
sensor.record(21.8)
print(f"\nСредняя температура: {sensor.average():.1f}°{sensor.unit}")