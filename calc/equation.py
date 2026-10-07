"""Расчётная часть: решение уравнения A*x^2 + B*x + C = 0."""

import math

# Допустимый модуль коэффициентов (свойство уравнения)
MAX_VALUE = 10000


def check_coefficients(coefficients):
    """Проверить коэффициенты; недопустимые данные — ValueError.

    coefficients: словарь {"A": число, "B": число, "C": число}.
    """
    for name, value in coefficients.items():
        if abs(value) > MAX_VALUE:
            raise ValueError(
                f"коэффициент {name} вне допустимого диапазона "
                f"[-{MAX_VALUE}; {MAX_VALUE}]"
            )

    if coefficients["A"] == 0 and coefficients["B"] == 0:
        raise ValueError("не уравнение: неизвестного нет")


def solve(a, b, c):
    """Решить уравнение; ничего не печатает.

    Возвращает кортеж (вид, дискриминант, список корней):
        квадратное, D > 0  ->  "квадратное", D, [x1, x2]
        квадратное, D = 0  ->  "квадратное", D, [x]
        квадратное, D < 0  ->  "квадратное", D, []
        линейное           ->  "линейное", None, [x]
    Предполагается, что коэффициенты уже проверены.
    """
    if a == 0:
        return "линейное", None, [-c / b]

    d = b * b - 4 * a * c

    if d < 0:
        return "квадратное", d, []

    if d == 0:
        return "квадратное", d, [-b / (2 * a)]

    root = math.sqrt(d)
    x1 = (-b + root) / (2 * a)
    x2 = (-b - root) / (2 * a)
    return "квадратное", d, [x1, x2]
