# Practice-03: Python Functions, Lambda, Classes & Inheritance

## Структура проекта

```
Practice-03/
├── functions/
│   ├── basic_functions.py      — базовые функции, рекурсия, docstring
│   ├── function_arguments.py   — позиционные, именованные, параметры по умолчанию
│   ├── return_values.py        — возврат значений, кортежей, словарей, функций
│   └── args_kwargs.py          — *args, **kwargs, распаковка
├── lambda/
│   ├── lambda_basics.py        — синтаксис лямбд, IIFE, списки лямбд
│   ├── lambda_with_map.py      — map() с лямбдами, матрицы
│   ├── lambda_with_filter.py   — filter() + конвейер map+filter
│   └── lambda_with_sorted.py   — sorted(), многоуровневая сортировка
├── classes/
│   ├── class_definition.py     — определение класса, объекты, __str__
│   ├── init_method.py          — __init__, self, вычисляемые атрибуты
│   ├── class_methods.py        — instance/class/@staticmethod, dunder-методы
│   └── class_variables.py      — class vs instance переменные, ловушки
├── inheritance/
│   ├── inheritance_basics.py   — наследование, isinstance, issubclass, цепочки
│   ├── super_function.py       — super() в __init__ и методах
│   ├── method_overriding.py    — переопределение, полиморфизм
│   └── multiple_inheritance.py — миксины, MRO, cooperative super()
└── README.md
```

## Ключевые концепции

### Functions
| Концепция | Описание |
|-----------|----------|
| `def` | Определение функции |
| `return` | Возврат одного или нескольких значений (кортеж) |
| `*args` | Произвольное количество позиционных аргументов |
| `**kwargs` | Произвольное количество именованных аргументов |
| Параметры по умолчанию | `def f(x, y=10)` |
| Замыкания | Функция, возвращающая функцию |

### Lambda
| Концепция | Описание |
|-----------|----------|
| `lambda x: expr` | Анонимная функция |
| `map(f, iterable)` | Применить функцию к каждому элементу |
| `filter(f, iterable)` | Оставить элементы, где f возвращает True |
| `sorted(lst, key=f)` | Сортировка с ключом |

### Classes
| Концепция | Описание |
|-----------|----------|
| `class Name:` | Определение класса |
| `__init__(self, ...)` | Конструктор — вызывается при создании объекта |
| Переменная класса | Общая для всех экземпляров |
| Переменная экземпляра | Уникальная для каждого объекта (через `self`) |
| `@classmethod` | Метод класса, получает `cls` |
| `@staticmethod` | Статический метод, не получает `self`/`cls` |
| Dunder-методы | `__str__`, `__repr__`, `__add__`, `__eq__` и др. |

### Inheritance
| Концепция | Описание |
|-----------|----------|
| `class Child(Parent)` | Одиночное наследование |
| `class Child(P1, P2)` | Множественное наследование |
| `super()` | Доступ к родительскому классу |
| Переопределение метода | Дочерний класс заменяет метод родителя |
| MRO | Method Resolution Order — порядок поиска методов |
| Mixin | Класс, добавляющий функциональность через множественное наследование |

## Запуск примеров

```bash
# Запустить отдельный файл
python functions/basic_functions.py

# Запустить все файлы одной командой (bash)
for f in functions/*.py lambda/*.py classes/*.py inheritance/*.py; do
    echo "=== $f ==="; python "$f"; echo
done
```

## Git-инструкции для сдачи

```bash
git add .
git commit -m "Complete Practice 3: Python functions, lambda, classes, and inheritance examples"
git push origin main
```