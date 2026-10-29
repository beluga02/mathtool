"""Расчётная часть: сортировки списка целых чисел.

Каждая сортировка изменяет переданный список и возвращает None.
Параметр descending=True задаёт порядок по убыванию.
"""

from calc.arrays import MAX_VALUE, MIN_VALUE


def out_of_order(a, b, descending):
    """Верно, если пара a, b (a стоит левее) расположена не по порядку."""
    if descending:
        return a < b
    return a > b


def bubble(values, descending=False):
    """Сортировка пузырьком с досрочным выходом."""
    n = len(values)
    for i in range(n - 1):
        swapped = False
        # После каждого прохода наибольший (наименьший) элемент встаёт на место
        for j in range(n - 1 - i):
            if out_of_order(values[j], values[j + 1], descending):
                values[j], values[j + 1] = values[j + 1], values[j]
                swapped = True
        if not swapped:
            break


def selection(values, descending=False):
    """Сортировка выбором."""
    n = len(values)
    for i in range(n - 1):
        # Ищем элемент, который должен стоять на позиции i
        best = i
        for j in range(i + 1, n):
            if out_of_order(values[best], values[j], descending):
                best = j
        values[i], values[best] = values[best], values[i]


def insertion(values, descending=False):
    """Сортировка вставками."""
    for i in range(1, len(values)):
        current = values[i]
        j = i
        # Сдвигаем элементы, стоящие не по порядку, вправо
        while j > 0 and out_of_order(values[j - 1], current, descending):
            values[j] = values[j - 1]
            j -= 1
        values[j] = current


def counting(values, descending=False):
    """Сортировка подсчётом для значений из [MIN_VALUE; MAX_VALUE]."""
    counters = [0] * (MAX_VALUE - MIN_VALUE + 1)
    for value in values:
        counters[value - MIN_VALUE] += 1

    # Порядок обхода счётчиков определяет направление сортировки
    if descending:
        indexes = range(len(counters) - 1, -1, -1)
    else:
        indexes = range(len(counters))

    k = 0
    for index in indexes:
        for _ in range(counters[index]):
            values[k] = index + MIN_VALUE
            k += 1




# Таблица методов: имя из командной строки -> функция сортировки
METHODS = {}
METHODS["bubble"] = bubble
METHODS["selection"] = selection
METHODS["insertion"] = insertion
METHODS["counting"] = counting
