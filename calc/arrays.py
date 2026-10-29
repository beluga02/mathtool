"""Расчётная часть: массивы целых чисел — генерация, проверка, поиск."""

import random

# Допустимые значения элементов и размер массива
MIN_VALUE = -100
MAX_VALUE = 100
MAX_COUNT = 1_000_000

# Наибольший модуль искомого числа
MAX_SEARCH = 1000


def check_count(count):
    """Проверить количество элементов; недопустимое — ValueError."""
    if not 1 <= count <= MAX_COUNT:
        raise ValueError(
            f"количество элементов вне диапазона [1; {MAX_COUNT}]"
        )


def check_bounds(low, high):
    """Проверить границы значений при генерации; недопустимые — ValueError."""
    for name, value in (("--min", low), ("--max", high)):
        if not MIN_VALUE <= value <= MAX_VALUE:
            raise ValueError(
                f"значение {name} вне диапазона [{MIN_VALUE}; {MAX_VALUE}]"
            )
    if low > high:
        raise ValueError("--min не может быть больше --max")


def check_values(values):
    """Проверить прочитанный массив: количество и диапазон значений."""
    check_count(len(values))
    for value in values:
        if not MIN_VALUE <= value <= MAX_VALUE:
            raise ValueError(
                f"значение {value} вне диапазона [{MIN_VALUE}; {MAX_VALUE}]"
            )


def check_sorted(values):
    """Проверить порядок по возрастанию; нарушение — ValueError."""
    for i in range(len(values) - 1):
        if values[i] > values[i + 1]:
            raise ValueError("массив не упорядочен по возрастанию")


def check_search_value(value):
    """Проверить искомое число; недопустимое — ValueError."""
    if abs(value) > MAX_SEARCH:
        raise ValueError(f"модуль искомого числа больше {MAX_SEARCH}")


def fill(count, low=MIN_VALUE, high=MAX_VALUE, seed=None):
    """Создать список из count случайных целых из [low; high].

    seed — начальное значение генератора (None — не задано).
    """
    generator = random.Random(seed)
    values = []
    for _ in range(count):
        values.append(generator.randint(low, high))
    return values


def binary_search(values, target):
    """Двоичный поиск в массиве по возрастанию.

    Возвращает индекс с нуля любого вхождения или None.
    """
    left = 0
    right = len(values) - 1
    while left <= right:
        middle = (left + right) // 2
        if values[middle] == target:
            return middle
        if values[middle] < target:
            left = middle + 1
        else:
            right = middle - 1
    return None


def is_ascending(values):
    """True, если каждый элемент не больше следующего."""
    for i in range(len(values) - 1):
        if values[i] > values[i + 1]:
            return False
    return True
