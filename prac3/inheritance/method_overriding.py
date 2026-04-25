# ============================================================
# method_overriding.py — Переопределение методов (Method Overriding)
# ============================================================
# Дочерний класс может переопределить метод родителя,
# предоставив свою реализацию с тем же именем.

# ── 1. Базовый пример переопределения ────────────────────────
class Animal:
    def sound(self):
        return "Какой-то звук"

    def description(self):
        return f"Я {type(self).__name__} и издаю звук: {self.sound()}"


class Dog(Animal):
    def sound(self):          # переопределяем метод родителя
        return "Гав-гав!"


class Cat(Animal):
    def sound(self):          # переопределяем метод родителя
        return "Мяу!"


class Duck(Animal):
    def sound(self):
        return "Кря-кря!"


# description() вызывает self.sound() — полиморфизм
animals = [Dog(), Cat(), Duck(), Animal()]
for animal in animals:
    print(animal.description())
# Я Dog и издаю звук: Гав-гав!
# Я Cat и издаю звук: Мяу!
# Я Duck и издаю звук: Кря-кря!
# Я Animal и издаю звук: Какой-то звук


# ── 2. Полиморфизм через переопределение ─────────────────────
class Shape:
    def area(self):
        raise NotImplementedError("Подкласс обязан реализовать area()")

    def perimeter(self):
        raise NotImplementedError("Подкласс обязан реализовать perimeter()")

    def info(self):
        return f"{type(self).__name__}: площадь={self.area():.2f}, периметр={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        import math
        return math.pi * self.radius ** 2

    def perimeter(self):
        import math
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c

    def area(self):
        s = self.perimeter() / 2  # полупериметр
        return (s * (s-self.a) * (s-self.b) * (s-self.c)) ** 0.5

    def perimeter(self):
        return self.a + self.b + self.c


shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
print("\n--- Фигуры ---")
for shape in shapes:
    print(shape.info())


# ── 3. Переопределение __str__ и __repr__ ────────────────────
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def __str__(self):
        return f"Vehicle: {self.brand}"

    def __repr__(self):
        return f"Vehicle(brand={self.brand!r})"


class ElectricVehicle(Vehicle):
    def __init__(self, brand, range_km):
        super().__init__(brand)
        self.range_km = range_km

    def __str__(self):   # переопределяем строковое представление
        return f"EV: {self.brand} (запас хода: {self.range_km} км)"

    def __repr__(self):
        return f"ElectricVehicle(brand={self.brand!r}, range_km={self.range_km})"


v = Vehicle("Ford")
ev = ElectricVehicle("Tesla", 450)
print(f"\n{v}")       # Vehicle: Ford
print(f"{ev}")        # EV: Tesla (запас хода: 450 км)
print(repr(ev))       # ElectricVehicle(brand='Tesla', range_km=450)


# ── 4. Переопределение с расширением логики ───────────────────
class BaseProcessor:
    def process(self, data):
        print(f"[Base] Обрабатываю: {data}")
        return data.strip()


class UpperCaseProcessor(BaseProcessor):
    def process(self, data):
        result = super().process(data)   # вызываем родителя
        return result.upper()            # добавляем свою логику


class CensorProcessor(UpperCaseProcessor):
    BAD_WORDS = ["спам", "СПАМ"]

    def process(self, data):
        result = super().process(data)   # вызываем цепочку super()
        for word in self.BAD_WORDS:
            result = result.replace(word.upper(), "***")
        return result


p1 = BaseProcessor()
p2 = UpperCaseProcessor()
p3 = CensorProcessor()

text = "  привет, это спам  "
print(f"\nBase:       '{p1.process(text)}'")
print(f"UpperCase:  '{p2.process(text)}'")
print(f"Censor:     '{p3.process(text)}'")
# Base:       'привет, это спам'
# UpperCase:  'ПРИВЕТ, ЭТО СПАМ'
# Censor:     'ПРИВЕТ, ЭТО ***'