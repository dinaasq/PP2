# ============================================================
# inheritance_basics.py — Основы наследования
# ============================================================
# Синтаксис: class Child(Parent):
# Дочерний класс наследует все атрибуты и методы родителя

# ── Базовый пример: Animal → Dog, Cat ────────────────────────
class Animal:
    """Базовый (родительский) класс для всех животных."""

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def breathe(self):
        print(f"{self.name} дышит воздухом.")

    def eat(self):
        print(f"{self.name} ест.")

    def sleep(self):
        print(f"{self.name} спит.")

    def __str__(self):
        return f"{type(self).__name__}(name={self.name}, age={self.age})"


class Dog(Animal):
    """Дочерний класс — Собака наследует Animal."""

    def bark(self):
        """Метод, специфичный для собаки."""
        print(f"{self.name}: Гав-гав!")

    def fetch(self, item):
        print(f"{self.name} принёс {item}!")


class Cat(Animal):
    """Дочерний класс — Кошка наследует Animal."""

    def meow(self):
        print(f"{self.name}: Мяу-мяу!")

    def purr(self):
        print(f"{self.name} мурлычет...")


# Объекты дочерних классов имеют методы и родителя, и свои
dog = Dog("Шарик", 3)
cat = Cat("Мурзик", 5)

dog.breathe()   # из Animal
dog.eat()       # из Animal
dog.bark()      # из Dog
dog.fetch("мячик")  # из Dog

print()
cat.sleep()     # из Animal
cat.meow()      # из Cat
cat.purr()      # из Cat

print(dog)   # Dog(name=Шарик, age=3)
print(cat)   # Cat(name=Мурзик, age=5)


# ── Проверка наследования ────────────────────────────────────
print("\n--- Проверки типов ---")
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True — Dog является подтипом Animal
print(isinstance(cat, Dog))     # False
print(issubclass(Dog, Animal))  # True
print(issubclass(Cat, Animal))  # True
print(issubclass(Dog, Cat))     # False


# ── Глубокое наследование: цепочка классов ───────────────────
class Vehicle:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed  # макс. скорость (км/ч)

    def describe(self):
        return f"{self.brand}, макс. скорость: {self.speed} км/ч"


class Car(Vehicle):
    def __init__(self, brand, speed, doors):
        super().__init__(brand, speed)
        self.doors = doors

    def describe(self):
        return super().describe() + f", {self.doors} дверей"


class ElectricCar(Car):
    """Электромобиль — наследует Car, который наследует Vehicle."""

    def __init__(self, brand, speed, doors, battery_kwh):
        super().__init__(brand, speed, doors)
        self.battery_kwh = battery_kwh

    def describe(self):
        return super().describe() + f", батарея: {self.battery_kwh} кВт·ч"

    def charge(self):
        print(f"{self.brand}: Зарядка началась...")


tesla = ElectricCar("Tesla Model 3", 225, 4, 82)
print(f"\n{tesla.describe()}")
# Tesla Model 3, макс. скорость: 225 км/ч, 4 дверей, батарея: 82 кВт·ч
tesla.charge()

# Цепочка: ElectricCar → Car → Vehicle
print(ElectricCar.__mro__)
# (<class 'ElectricCar'>, <class 'Car'>, <class 'Vehicle'>, <class 'object'>)