# ============================================================
# class_variables.py — Переменные класса vs переменные экземпляра
# ============================================================
#
# CLASS VARIABLE    — одна на весь класс, общая для всех объектов
# INSTANCE VARIABLE — отдельная для каждого объекта
# ============================================================

# ── Пример 1: счётчик экземпляров через переменную класса ───
class Employee:
    # Переменная КЛАССА — общий счётчик
    employee_count = 0
    company_name = "ТехноКорп"

    def __init__(self, name, department, salary):
        # Переменные ЭКЗЕМПЛЯРА — уникальны для каждого объекта
        self.name = name
        self.department = department
        self.salary = salary
        # Изменяем переменную класса при создании объекта
        Employee.employee_count += 1
        self.employee_id = Employee.employee_count  # уникальный ID

    def info(self):
        return (f"ID:{self.employee_id} | {self.name} | "
                f"{self.department} | {self.salary:,}₸")

    @classmethod
    def get_company_info(cls):
        return f"{cls.company_name}: {cls.employee_count} сотрудников"

    def __del__(self):
        Employee.employee_count -= 1

# Создаём сотрудников
e1 = Employee("Айгерим", "IT", 350000)
e2 = Employee("Нұрлан", "HR", 280000)
e3 = Employee("Мария", "Finance", 310000)

print(Employee.get_company_info())  # ТехноКорп: 3 сотрудников
print(e1.info())  # ID:1 | Айгерим | IT | 350,000₸
print(e2.info())  # ID:2 | Нұрлан | HR | 280,000₸

# Доступ к переменной класса через экземпляр (читается, но лучше через класс)
print(e1.company_name)      # ТехноКорп
print(Employee.company_name)  # ТехноКорп


# ── Пример 2: опасность «затенения» переменной класса ────────
print("\n--- Затенение переменной класса ---")

class Config:
    DEBUG = False      # переменная КЛАССА

c1 = Config()
c2 = Config()

# Изменяем через класс — меняется у ВСЕХ
Config.DEBUG = True
print(f"c1.DEBUG = {c1.DEBUG}")   # True
print(f"c2.DEBUG = {c2.DEBUG}")   # True

# Присваиваем через экземпляр — создаётся переменная ЭКЗЕМПЛЯРА (shadow!)
c1.DEBUG = False
print(f"\nПосле c1.DEBUG = False:")
print(f"c1.DEBUG = {c1.DEBUG}")      # False (переменная экземпляра c1)
print(f"c2.DEBUG = {c2.DEBUG}")      # True  (переменная класса не изменилась)
print(f"Config.DEBUG = {Config.DEBUG}")  # True

# Проверяем, есть ли переменная в __dict__ экземпляра
print(f"\nc1.__dict__ = {c1.__dict__}")  # {'DEBUG': False} — есть своя
print(f"c2.__dict__ = {c2.__dict__}")   # {}              — своей нет


# ── Пример 3: изменяемые переменные класса — ловушка! ─────────
print("\n--- Ловушка: изменяемая переменная класса ---")

class BadClass:
    shared_list = []   # ОПАСНО: один список для всех объектов!

class GoodClass:
    def __init__(self):
        self.own_list = []  # ПРАВИЛЬНО: у каждого объекта свой список

b1 = BadClass()
b2 = BadClass()
b1.shared_list.append("данные от b1")
print(f"b2.shared_list: {b2.shared_list}")  # ['данные от b1'] — неожиданно!

g1 = GoodClass()
g2 = GoodClass()
g1.own_list.append("данные от g1")
print(f"g2.own_list: {g2.own_list}")   # []  — изолировано, как надо


# ── Пример 4: практический случай — синглтон-счётчик ──────────
print("\n--- Синглтон-счётчик ID ---")

class Order:
    _next_id = 1000   # переменная класса — генератор ID

    def __init__(self, product, quantity):
        self.order_id = f"ORD-{Order._next_id}"
        Order._next_id += 1
        self.product = product
        self.quantity = quantity

    def __str__(self):
        return f"{self.order_id}: {self.quantity}x {self.product}"

orders = [
    Order("Ноутбук", 1),
    Order("Мышь", 3),
    Order("Монитор", 2),
]
for order in orders:
    print(order)
# ORD-1000: 1x Ноутбук
# ORD-1001: 3x Мышь
# ORD-1002: 2x Монитор