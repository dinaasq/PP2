# ============================================================
# super_function.py — Функция super()
# ============================================================
# super() возвращает прокси-объект для родительского класса.
# Позволяет вызывать методы родителя без явного указания его имени.

# ── 1. super().__init__() — расширение конструктора ──────────
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        print(f"  [Person.__init__] name={name}, age={age}")

    def introduce(self):
        return f"Меня зовут {self.name}, мне {self.age} лет."


class Student(Person):
    def __init__(self, name, age, university, gpa):
        # Вызываем __init__ родителя, чтобы инициализировать name и age
        super().__init__(name, age)
        # Добавляем собственные атрибуты
        self.university = university
        self.gpa = gpa
        print(f"  [Student.__init__] university={university}, gpa={gpa}")

    def introduce(self):
        base = super().introduce()  # получаем строку от родителя
        return f"{base} Учусь в {self.university}, GPA: {self.gpa}"


print("Создаём студента:")
s = Student("Айгерим", 20, "КазНУ", 3.8)
print(s.introduce())
# Меня зовут Айгерим, мне 20 лет. Учусь в КазНУ, GPA: 3.8


# ── 2. super() в цепочке трёх уровней ────────────────────────
class Shape:
    def __init__(self, color="белый"):
        self.color = color

    def describe(self):
        return f"Фигура цвета '{self.color}'"


class Polygon(Shape):
    def __init__(self, color, sides):
        super().__init__(color)
        self.sides = sides

    def describe(self):
        parent_desc = super().describe()
        return f"{parent_desc}, {self.sides} сторон"


class RegularPolygon(Polygon):
    def __init__(self, color, sides, side_length):
        super().__init__(color, sides)
        self.side_length = side_length

    def describe(self):
        parent_desc = super().describe()
        return f"{parent_desc}, длина стороны: {self.side_length}"

    def perimeter(self):
        return self.sides * self.side_length


rp = RegularPolygon("синий", 6, 5)
print(f"\n{rp.describe()}")
# Фигура цвета 'синий', 6 сторон, длина стороны: 5
print(f"Периметр: {rp.perimeter()}")  # 30


# ── 3. super() для вызова метода родителя (не только __init__) ─
class Logger:
    def log(self, message):
        print(f"[LOG] {message}")


class TimestampLogger(Logger):
    def log(self, message):
        import datetime
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        # Вызываем родительский log(), добавляя временну́ю метку
        super().log(f"[{ts}] {message}")


class PrefixLogger(TimestampLogger):
    def __init__(self, prefix):
        self.prefix = prefix

    def log(self, message):
        # Добавляем префикс и вызываем цепочку super()
        super().log(f"{self.prefix}: {message}")


logger = PrefixLogger("APP")
logger.log("Приложение запущено")
# [LOG] [14:30:01] APP: Приложение запущено


# ── 4. super() в __str__ ─────────────────────────────────────
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def __str__(self):
        return f"Animal({self.name})"

    def speak(self):
        return f"{self.name} говорит '{self.sound}'"


class Pet(Animal):
    def __init__(self, name, sound, owner):
        super().__init__(name, sound)
        self.owner = owner

    def __str__(self):
        animal_str = super().__str__()   # "Animal(Барсик)"
        return f"Pet({animal_str}, owner={self.owner})"

    def speak(self):
        base = super().speak()
        return f"{base} (питомец {self.owner})"


pet = Pet("Барсик", "мяу", "Мария")
print(f"\n{pet}")           # Pet(Animal(Барсик), owner=Мария)
print(pet.speak())          # Барсик говорит 'мяу' (питомец Мария)