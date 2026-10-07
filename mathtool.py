"""Точка входа: выбор команды, ввод и вывод."""

import sys

import cli
from calc import equation, integration, series, stats

NOT_EXISTS = "НЕ СУЩЕСТВУЕТ"

# Таблица показателей stats: (подпись, функция, формат).
# Первая строка — не показатель, а количество прочитанных чисел.
REPORT = [
    ("Количество", len, "d"),
    ("Сумма", stats.total, ".3f"),
    ("Ср. арифм.", stats.mean, ".3f"),
    ("Сумма кв.", stats.sum_squares, ".3f"),
    ("Ср. кв.", stats.rms, ".3f"),
    ("Дисперсия", stats.variance, ".3f"),
    ("СКО", stats.sko, ".3f"),
    ("Станд. откл.", stats.std, ".3f"),
    ("Наименьшее", stats.minimum, ".3f"),
    ("Наибольшее", stats.maximum, ".3f"),
    ("Положительных", stats.count_positive, "d"),
    ("Отрицательных", stats.count_negative, "d"),
]


# --- Вспомогательные функции ввода-вывода ---

def format_value(value, form):
    """Отформатировать значение; «-0.000» заменяется на «0.000»."""
    text = f"{value:{form}}"
    if text.startswith("-") and not any(ch in "123456789" for ch in text):
        text = text[1:]
    return text


def read_coefficient(name):
    """Запросить коэффициент с клавиатуры."""
    try:
        return int(input(f"Введите {name}: "))
    except ValueError:
        raise ValueError(f"коэффициент {name} не является целым числом")
    except EOFError:
        raise ValueError(f"не удалось прочитать коэффициент {name}")


def read_values(source):
    """Прочитать числа из источника (файл или стандартный ввод)."""
    values = []
    for line in source:
        for word in line.split():
            try:
                values.append(float(word))
            except ValueError:
                raise ValueError(f"'{word}' не является числом")
    return values


# --- Обработчики команд: возвращают код завершения ---

def handle_solve(args):
    """Команда solve."""
    given = [args.a, args.b, args.c]

    if all(value is None for value in given):
        a = read_coefficient("A")
        b = read_coefficient("B")
        c = read_coefficient("C")
    elif any(value is None for value in given):
        raise ValueError("необходимо указать параметры -a, -b и -c")
    else:
        a, b, c = given

    equation.check_coefficients({"A": a, "B": b, "C": c})
    kind, discriminant, roots = equation.solve(a, b, c)

    print(f"Уравнение {kind}")
    if discriminant is not None:
        print(f"Дискриминант: {discriminant}")

    if len(roots) == 0:
        print("Действительных корней нет")
    elif len(roots) == 1:
        print(f"Корень: x = {format_value(roots[0], '.3f')}")
    else:
        print(f"x1 = {format_value(roots[0], '.3f')}")
        print(f"x2 = {format_value(roots[1], '.3f')}")

    return 0


def handle_stats(args):
    """Команда stats."""
    if args.input is not None:
        with open(args.input, encoding="utf-8-sig") as handle:
            values = read_values(handle)
    else:
        if sys.stdin.isatty():
            print(
                "Введите числа через пробел или с новой строки. "
                "Конец ввода: Ctrl+D (Windows: Ctrl+Z, Enter).",
                file=sys.stderr
            )
        values = read_values(sys.stdin)

    stats.check_values(values)

    for label, function, form in REPORT:
        value = function(values)
        if value is None:
            print(f"{label}: {NOT_EXISTS}")
        else:
            print(f"{label}: {format_value(value, form)}")

    return 0


def handle_series(args):
    """Команда series."""
    term, formula = series.FORMULAS[args.func]

    if args.terms is not None:
        series.check_terms(args.terms)
        result = series.sum_by_count(term, args.terms)
        count = args.terms
    else:
        series.check_eps(args.eps)
        result, count = series.sum_by_eps(term, args.eps)

    print(formula)
    print(f"Слагаемых: {count}")
    print(f"Сумма ряда: {result:.{series.DIGITS}f}")

    return 0


def handle_integrate(args):
    """Команда integrate."""
    function, formula, _, _, _ = integration.FUNCTIONS[args.func]

    # Проверка — до вывода формулы
    integration.check_limits(args.func, args.start, args.end, args.steps)
    result = integration.integral(function, args.start, args.end, args.steps)

    print(formula)
    print(f"Значение интеграла: {format_value(result, f'.{series.DIGITS}f')}")

    return 0


HANDLERS = {
    "solve": handle_solve,
    "stats": handle_stats,
    "series": handle_series,
    "integrate": handle_integrate,
}


def main(argv):
    """Разобрать параметры, вызвать обработчик, вернуть код завершения."""
    parser = cli.build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

    try:
        return HANDLERS[args.command](args)
    except (ValueError, OSError) as error:
        print(f"ОШИБКА: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
