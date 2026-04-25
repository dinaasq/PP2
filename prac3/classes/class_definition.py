# ============================================================
# class_definition.py — Определение классов и создание объектов
# ============================================================

# 1. Минимальный класс
class Dog:
    pass  # пустой класс — тело можно оставить пустым

my_dog = Dog()  # создание объекта (экземпляра класса)
print(type(my_dog))   # <class '__main__.Dog'>
print(isinstance(my_dog, Dog))  # True


# 2. Класс с атрибутами и методом
class Car:
    """Класс, описывающий автомобиль."""

    # Атрибуты экземпляра задаются через __init__
    def __init__(self, make, model, year):
        self.make = make    # марка
        self.model = model  # модель
        self.year = year    # год выпуска

    def description(self):
        """Возвращает строковое описание автомобиля."""
        return f"{self.year} {self.make} {self.model}"

    def start(self):
        print(f"{self.make} {self.model}: Двигатель запущен! 🚗")

# Создаём объекты
car1 = Car("Toyota", "Camry", 2022)
car2 = Car("BMW", "X5", 2023)

print(car1.description())   # 2022 Toyota Camry
print(car2.description())   # 2023 BMW X5
car1.start()                # Toyota Camry: Двигатель запущен! 🚗


# 3. Доступ и изменение атрибутов
print(f"\nМарка: {car1.make}")      # Toyota
car1.year = 2024                    # изменяем атрибут
print(f"Новый год: {car1.year}")    # 2024

# Добавление нового атрибута динамически
car1.color = "белый"
print(f"Цвет: {car1.color}")   # белый


# 4. Удаление атрибута
del car1.color
# print(car1.color)  # AttributeError — атрибут удалён


# 5. Класс Person с несколькими методами
class Person:
    """Класс для представления человека."""

    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def introduce(self):
        print(f"Меня зовут {self.full_name()}, мне {self.age} лет.")

    def birthday(self):
        """Увеличивает возраст на 1 год."""
        self.age += 1
        print(f"С днём рождения, {self.first_name}! Тебе теперь {self.age}.")

    def __str__(self):
        """Читаемое строковое представление объекта."""
        return f"Person({self.full_name()}, {self.age} лет)"

# Создаём объекты Person
person1 = Person("Айгерим", "Сатпаева", 25)
person2 = Person("Данияр", "Кенжебаев", 30)

person1.introduce()   # Меня зовут Айгерим Сатпаева, мне 25 лет.
person2.introduce()   # Меня зовут Данияр Кенжебаев, мне 30 лет.

person1.birthday()    # С днём рождения, Айгерим! Тебе теперь 26.
print(person1)        # Person(Айгерим Сатпаева, 26 лет)
print(person2)        # Person(Данияр Кенжебаев, 30 лет)


# 6. Список объектов
team = [
    Person("Алина", "Иванова", 22),
    Person("Максим", "Петров", 28),
    Person("Зарина", "Асанова", 24),
]
print("\nКоманда:")
for member in team:
    print(f"  {member}")