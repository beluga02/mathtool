"""Разбор параметров командной строки."""

import argparse

from calc import arrays, integration, series, sorting
from calc.arrays import MIN_VALUE, MAX_VALUE
from calc.sorting import METHODS


def build_parser():
    """Создать разборщик параметров приложения и вернуть его."""
    parser = argparse.ArgumentParser(
        prog="mathtool",
        description="mathtool — расчёты над уравнениями "
                    "и числовыми последовательностями",
        allow_abbrev=False,
    )
    commands = parser.add_subparsers(dest="command", title="команды")

    # --- solve: уравнение A*x^2 + B*x + C = 0 ---
    solve = commands.add_parser(
        "solve", allow_abbrev=False,
        help="решить уравнение A*x^2 + B*x + C = 0",
        description="Решение уравнения A*x^2 + B*x + C = 0. Без -a, -b, -c "
                    "коэффициенты запрашиваются с клавиатуры.",
    )
    solve.add_argument("-a", type=int, help="коэффициент A (целое)")
    solve.add_argument("-b", type=int, help="коэффициент B (целое)")
    solve.add_argument("-c", type=int, help="коэффициент C (целое)")

    # --- stats: показатели последовательности ---
    stats = commands.add_parser(
        "stats", allow_abbrev=False,
        help="показатели числовой последовательности",
        description="Числа читаются из файла или со стандартного ввода.",
    )
    stats.add_argument(
        "--input",
        help="файл с числами (без него — стандартный ввод)",
    )

    # --- series: сумма ряда ---
    series_parser = commands.add_parser(
        "series", allow_abbrev=False,
        help="сумма знакочередующегося ряда",
        description="Сумма ряда: остановка по количеству слагаемых "
                    "или по точности.",
    )
    series_parser.add_argument(
        "--func", required=True, choices=sorted(series.FORMULAS),
        help="какой ряд суммировать",
    )
    stop = series_parser.add_mutually_exclusive_group(required=True)
    stop.add_argument(
        "--terms", type=int,
        help="сколько слагаемых сложить (целое от 1 до 10000)",
    )
    stop.add_argument(
        "--eps", type=float,
        help="считать, пока слагаемое по модулю не станет меньше eps "
             "(0 < eps <= 0.0001)",
    )

    # --- integrate: численное интегрирование ---
    integrate = commands.add_parser(
        "integrate", allow_abbrev=False,
        help="интеграл методом левых прямоугольников",
        description="Численное интегрирование методом левых прямоугольников.",
    )
    integrate.add_argument(
        "--func", required=True, choices=sorted(integration.FUNCTIONS),
        help="какую функцию интегрировать",
    )
    integrate.add_argument(
        "--from", dest="start", type=float, required=True,
        help="нижний предел интегрирования",
    )
    integrate.add_argument(
        "--to", dest="end", type=float, required=True,
        help="верхний предел интегрирования (больше нижнего)",
    )
    integrate.add_argument(
        "--steps", type=int, required=True,
        help="число прямоугольников (целое от 1 до 100000)",
    )

    # --- fill: заполнение массива случайными числами ---
    fill = commands.add_parser(
        "fill", allow_abbrev=False,
        help="создать массив случайных целых чисел",
        description="Создание массива случайных целых чисел.",
    )
    fill.add_argument(
        "-c", "--count", type=int, required=True,
        help=f"количество элементов (от 1 до {arrays.MAX_COUNT})",
    )
    fill.add_argument(
        "--min", dest="low", type=int, default=arrays.MIN_VALUE,
        help=f"нижняя граница значений (по умолчанию {arrays.MIN_VALUE})",
    )
    fill.add_argument(
        "--max", dest="high", type=int, default=arrays.MAX_VALUE,
        help=f"верхняя граница значений (по умолчанию {arrays.MAX_VALUE})",
    )
    fill.add_argument(
        "--seed", type=int,
        help="начальное значение генератора (целое; по умолчанию не задано)",
    )
    fill.add_argument(
        "-o", "--output",
        help="файл для массива (по умолчанию вывод на экран)",
    )

    # --- sort: сортировка массива ---
    sort = commands.add_parser(
        "sort", allow_abbrev=False,
        help="отсортировать массив",
        description="Сортировка массива целых чисел.",
    )
    sort.add_argument(
        "-m", "--method", required=True, choices=sorted(sorting.METHODS),
        help="метод сортировки",
    )
    sort.add_argument(
        "--order", choices=("asc", "desc"), default="asc",
        help="asc — по возрастанию, desc — по убыванию (по умолчанию asc)",
    )
    sort.add_argument(
        "-i", "--input",
        help="файл с массивом (по умолчанию ввод с клавиатуры)",
    )
    sort.add_argument(
        "-o", "--output",
        help="файл для результата (по умолчанию вывод на экран)",
    )

    # --- search: двоичный поиск ---
    search = commands.add_parser(
        "search", allow_abbrev=False,
        help="найти число в массиве по возрастанию",
        description="Двоичный поиск в массиве, упорядоченном по возрастанию.",
    )
    search.add_argument(
        "-v", "--value", type=int, required=True,
        help=f"искомое целое число (модуль не больше {arrays.MAX_SEARCH})",
    )
    search.add_argument(
        "-i", "--input",
        help="файл с массивом (по умолчанию ввод с клавиатуры)",
    )


    return parser


