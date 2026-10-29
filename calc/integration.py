"""Расчётная часть: интегрирование методом левых прямоугольников."""

import math
from calc import equation

# Допустимое число шагов
MAX_STEPS = 100000


def f_ratio(x):
    """F(x) = x / (x + 1)."""
    return x / (x + 1)


def f_root(x):
    """F(x) = sqrt(x^2 + 1)."""
    return math.sqrt(x * x + 1)

def f_test(x):
    # "F(x) = -x ** 2 + x + 2"
    return -x ** 2 + x + 2

x1 = equation.solve(-1, 1, 2)
# ["квадратное", d, [x1, x2]]
# ["квадратное", d, [x1, x2]]
# print(x1[2][0])
# print(x1[2][1])
# Таблица функций:
# имя -> (функция, формула, нижняя граница, верхняя граница, границы допустимы)
FUNCTIONS = {
    "ratio": (f_ratio, "F(x) = x / (x + 1)", 0, 20, True),
    "root": (f_root, "F(x) = sqrt(x^2 + 1)", -5, 5, False),
    "test": (f_test, "F(x) = -x ** 2 + x + 2", x1[2][0], x1[2][1], True)
}


def interval_text(name):
    """Запись промежутка функции: [a; b] или (a; b)."""
    _, _, low, high, closed = FUNCTIONS[name]
    if closed:
        return f"[{low}; {high}]"
    return f"({low}; {high})"


def check_limits(name, start, end, steps):
    """Проверить пределы и число шагов; недопустимое — ValueError."""
    if not (math.isfinite(start) and math.isfinite(end)):
        raise ValueError("пределы интегрирования должны быть конечными числами")

    if start >= end:
        raise ValueError("верхний предел --to должен быть больше нижнего --from")

    _, _, low, high, closed = FUNCTIONS[name]

    for parameter, value in (("--from", start), ("--to", end)):
        if closed:
            outside = value < low or value > high
        else:
            outside = value <= low or value >= high
        if outside:
            raise ValueError(
                f"значение {parameter} вне допустимого промежутка "
                f"{interval_text(name)} функции {name}"
            )

    if not 1 <= steps <= MAX_STEPS:
        raise ValueError(
            f"значение --steps должно находиться в диапазоне [1; {MAX_STEPS}]"
        )


def integral(function, a, b, steps):
    """Интеграл функции на [a; b] методом левых прямоугольников."""
    dx = (b - a) / steps
    result = 0
    for i in range(steps):
        x = a + i * dx
        result += function(x) * dx
    return result
