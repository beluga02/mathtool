"""Расчётная часть: сумма знакочередующегося ряда."""

import math

# Пределы команды
MAX_TERMS = 10000          # наибольшее значение --terms
MAX_EPS = 0.0001           # наибольшее (самое грубое) значение --eps
MAX_ITERATIONS = 100000    # предел повторений цикла суммирования по точности

# Число знаков при выводе суммы (разрешение формата, не гарантия точности)
DIGITS = math.ceil(-math.log10(MAX_EPS))


def sign(n):
    """Знак n-го слагаемого: нечётные +1, чётные -1."""
    if n % 2 == 0:
        return -1
    return 1


def term_sqplus(n):
    """Слагаемое ряда sqplus: знак / (n^2 + 1)."""
    return sign(n) / (n * n + 1)


def term_third(n):
    """Слагаемое ряда third: знак / (3 * n)."""
    return sign(n) / (3 * n)


# Таблица рядов: имя -> (функция слагаемого, запись формулы)
FORMULAS = {
    "sqplus": (term_sqplus, "S = 1/(1^2+1) - 1/(2^2+1) + 1/(3^2+1) - ..."),
    "third": (term_third, "S = 1/3 - 1/6 + 1/9 - 1/12 + ..."),
}


def check_terms(terms):
    """Проверить количество слагаемых; недопустимое — ValueError."""
    if not 1 <= terms <= MAX_TERMS:
        raise ValueError(
            f"значение --terms должно находиться в диапазоне [1; {MAX_TERMS}]"
        )


def check_eps(eps):
    """Проверить точность; недопустимая — ValueError."""
    if not (math.isfinite(eps) and 0 < eps <= MAX_EPS):
        raise ValueError(
            f"значение --eps должно быть конечным, больше нуля "
            f"и не больше {MAX_EPS}"
        )


def sum_by_count(term, count):
    """Сумма первых count слагаемых; term — функция слагаемого."""
    result = 0
    for n in range(1, count + 1):
        result += term(n)
    return result


def sum_by_eps(term, eps):
    """Сумма до слагаемого, меньшего eps по модулю (оно входит в сумму).

    Возвращает (сумма, количество слагаемых). Если за MAX_ITERATIONS
    повторений точность не достигнута — ValueError.
    """
    result = 0
    n = 0
    while True:
        n += 1
        value = term(n)
        result += value
        if abs(value) < eps:
            return result, n
        if n >= MAX_ITERATIONS:
            raise ValueError(
                f"точность {eps} не достигнута за {MAX_ITERATIONS} слагаемых"
            )
