"""Расчётная часть: показатели числовой последовательности.

Каждая функция получает список чисел и возвращает значение;
показатель, которого не существует, обозначается None.
"""

import math

# Ограничения на входные данные
MAX_COUNT = 20
MAX_ABS = 10000


def check_values(values):
    """Проверить список чисел; недопустимые данные — ValueError."""
    if len(values) == 0:
        raise ValueError("не получено ни одного числа")

    if len(values) > MAX_COUNT:
        raise ValueError(f"чисел больше допустимого количества ({MAX_COUNT})")

    for value in values:
        if not math.isfinite(value):
            raise ValueError(
                f"значение {value} не является конечным числом"
            )
        if abs(value) > MAX_ABS:
            raise ValueError(
                f"число {value} по модулю превышает {MAX_ABS}"
            )


def total(values):
    """Сумма чисел."""
    result = 0
    for value in values:
        result += value
    return result


def mean(values):
    """Среднее арифметическое."""
    return total(values) / len(values)


def sum_squares(values):
    """Сумма квадратов чисел."""
    result = 0
    for value in values:
        result += value ** 2
    return result


def rms(values):
    """Среднее квадратическое: корень из (сумма квадратов / N)."""
    return math.sqrt(sum_squares(values) / len(values))


def sum_squared_deviations(values):
    """Сумма квадратов отклонений от среднего (два прохода)."""
    mean_value = mean(values)
    result = 0
    for value in values:
        result += (value - mean_value) ** 2
    return result


def variance(values):
    """Дисперсия: сумма квадратов отклонений / N."""
    return sum_squared_deviations(values) / len(values)


def sko(values):
    """СКО: корень из дисперсии (отклонение по N)."""
    return math.sqrt(variance(values))


def std(values):
    """Стандартное отклонение (по N - 1); None, если чисел меньше двух."""
    if len(values) < 2:
        return None
    return math.sqrt(sum_squared_deviations(values) / (len(values) - 1))


def minimum(values):
    """Наименьшее число."""
    result = values[0]
    for value in values:
        if value < result:
            result = value
    return result


def maximum(values):
    """Наибольшее число."""
    result = values[0]
    for value in values:
        if value > result:
            result = value
    return result


def count_positive(values):
    """Количество чисел больше нуля."""
    result = 0
    for value in values:
        if value > 0:
            result += 1
    return result


def count_negative(values):
    """Количество чисел меньше нуля."""
    result = 0
    for value in values:
        if value < 0:
            result += 1
    return result
