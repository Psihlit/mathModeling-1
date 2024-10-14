import math
from random import randint, seed, uniform
from math import log, ceil
import matplotlib.pyplot as plt
import numpy as np


def generate_data(N: int, minimum_n=18, maximum_n=100, random_seed=True, type_of_numbers=True):
    """
    Функция для генерации случайного распределения возраста в возрасте от 18 до 100 лет
    :param N: количество генерируемых значений
    :param minimum_n: минимальное значение (по умолчанию 18)
    :param maximum_n: максимальное значение (по умолчанию 100)
    :param random_seed: определение семени генерации (если True - то каждый раз разное, иначе одинаковый сид)
    :return:
    """
    data = []

    if random_seed:
        seed(24)

    for i in range(1, N + 1):
        if type_of_numbers:
            random_number = randint(minimum_n, maximum_n)
        else:
            random_number = round(uniform(minimum_n, maximum_n), 2)
        new_tuple = (i, random_number)
        data.append(new_tuple)

    return data


def get_sample_mean(data):
    """
    Функция расчета выборочной средней (оценка математического ожидания случайной величины)
    :param data: выборка данных
    :return: выборочное среднее значение
    """
    summa = 0
    for i in range(len(data)):
        summa += data[i][1]
    return round(summa / len(data), 2)


def get_standard_deviation(data, sample_mean):
    """
    Функция для расчета среднего квадратического отклонения
    :param data: выборка данных
    :param sample_mean: выборочное среднее значение
    :return: среднее квадратическое отклонение
    """
    summa = 0

    for i in range(len(data)):
        summa += (data[i][1] - sample_mean) ** 2

    # Формула для расчета среднего квадратического отклонения
    variance = summa / len(data)  # Дисперсия
    return round(math.sqrt(variance), 2)  # Среднее квадратическое отклонение


def get_dispersion(standard_deviation):
    """
    Функция для расчета дисперсии
    :param standard_deviation: среднее квадратическое отклонение
    :return: дисперсия
    """
    return round(standard_deviation ** 2, 2)


def get_the_number_of_intervals_using_the_Sturgess_formula(N):
    """
    Функция для определения рекомендованного числа интервалов
    :param N: количество значений
    :return: округленное до большего целого число интервалов
    """
    return ceil(1 + 3.3221 * log(N))


def get_sample_size(data):
    """
    Функция для определения размаха
    :param data: выборка данных
    :return: размах выборки
    """
    minimum, maximum = data[0][1], data[0][1]
    for i in range(len(data)):
        if data[i][1] < minimum:
            minimum = data[i][1]
        if data[i][1] > maximum:
            maximum = data[i][1]
    return maximum - minimum


def get_size_of_the_intervals(R, n):
    """
    Функция для определения оптимальной длины интервалов
    :param R: размах выборки
    :param n: число интервалов выборки по формуле Стерджесса
    :return: округленная до большего целого длина интервалов
    """
    return ceil(R / n)


def get_intervals_with_frequency_distribution(a, n, delta_x, data):
    """
    Функция для определения интервалов и частоты значений в них
    :param a: минимальное значение интервала
    :param n: число интервалов
    :param delta_x: прирост значений между интервалами
    :param data: выборка данных
    :return: список кортежей типа (ai, bi, ni), где ai - значения интервала; bi - количество значений в интервале
    интервала; pi - частота значений в интервале;
    """
    intervals = []

    for i in range(n):
        new_tuple = (round(a, 2), round(a + delta_x, 2), 0)
        if new_tuple not in intervals:
            intervals.append(new_tuple)
        a += delta_x

    for i in range(len(data)):
        for j in range(len(intervals)):
            if intervals[j][0] <= data[i][1] <= intervals[j][1]:  # возможно первая проверка должна быть строгой
                intervals[j] = list(intervals[j])
                intervals[j][2] += 1
                intervals[j] = tuple(intervals[j])

    table = []  # итоговый список
    name = []  # список заголовков
    values = []  # список значений
    frequency = []  # список частот
    summa = 0  # переменная для подсчета общего количества значений

    # создание списков заголовков и значений
    for i in range(len(intervals)):
        name.append(f"{intervals[i][0]}-{intervals[i][1]}")
        values.append(intervals[i][2])
        summa += intervals[i][2]

    # добавление в конец колонки суммы
    name.append("Сумма")
    values.append(summa)

    try:
        # расчет частот для каждого интервала
        for i in range(len(name)):
            p = values[i] / values[-1]
            frequency.append(p)
    except ZeroDivisionError:
        print("Деление на ноль!")

    # создание итогового списка с объединенными значениями
    for i in range(len(name)):
        table.append((name[i], values[i], frequency[i]))

    return table


# def draw_empirical_cdf(data):
#     new_data = [value for _, value in data]  # Извлечение значений из кортежей
#
#     hist, edges = np.histogram(new_data, bins=len(new_data))
#     Y = hist.cumsum() / hist.sum()  # Нормализация на 1
#
#     # Линия для 0.0 слева от минимального значения
#     plt.plot([min(new_data) - 7, min(new_data)], [0.0, 0.0], c="blue")
#
#     for i in range(len(Y)):
#         plt.plot([edges[i], edges[i + 1]], [Y[i], Y[i]], c="blue")
#
#     # Линия для 1.0 справа от максимального значения
#     plt.plot([max(new_data), max(new_data) + 7], [Y[-1], Y[-1]], c="blue")
#
#     plt.title("Эмпирическая функция распределения")  # Заголовок графика
#     plt.xlabel("Значения случайной величины, X")  # Подпись оси X
#     plt.ylabel("Fn(X)")  # Подпись оси Y
#     plt.xticks(np.arange(min(new_data), max(new_data) + 2, 2), rotation=45)  # Деления по оси X каждые 2
#     plt.yticks(np.arange(0.0, 1.1, 0.1))  # Подписи по оси Y от 0.0 до 1.0
#     plt.grid(True)  # Добавление сетки для лучшей читабельности
#     plt.show()
#
#
# def draw_histogram(intervals):
#     intervals = intervals[0:-1]
#     # Извлекаем значения для осей X и Y
#     x_labels = [t[0] for t in intervals]  # Второй элемент кортежа для оси X
#     heights = [t[2] for t in intervals]  # Третий элемент кортежа для высоты столбцов
#
#     # Создаем фигуру и ось для графика
#     fig, ax = plt.subplots()
#
#     # Строим гистограмму
#     ax.bar(x_labels, heights, width=0.5, align='center')
#
#     # Добавляем подписи и заголовок
#     ax.set_xlabel('Интервалы')
#     ax.set_ylabel('Частота')
#     ax.set_title('Статистическая функция распределения')
#
#     # Устанавливаем метки по оси X
#     ax.set_xticks(x_labels)  # Устанавливаем позиции меток
#     ax.set_xticklabels(x_labels, rotation=45, ha='right')  # Устанавливаем метки и поворачиваем их
#
#     # Показываем график
#     plt.tight_layout()  # Автоматически подстраивает размещение графиков и меток
#     plt.show()


def draw_combined_graphs(data1=None, intervals1=None, data2=None, intervals2=None):
    """
    Функция для рисования графиков. В зависимости от входных данных, рисует графики:
    - Если есть только data1 и intervals1, рисует два графика в строке.
    - Если есть только data2 и intervals2, рисует два графика в строке.
    - Если есть оба набора данных, рисует четыре графика в сетке 2x2.

    :param data1: Первый набор данных для эмпирической функции распределения.
    :param intervals1: Первый набор интервалов для гистограммы.
    :param data2: Второй набор данных для эмпирической функции распределения.
    :param intervals2: Второй набор интервалов для гистограммы.
    """
    plt.close("all")
    # Определяем количество графиков
    num_plots = 0
    if data1 is not None and intervals1 is not None:
        num_plots += 2
    if data2 is not None and intervals2 is not None:
        num_plots += 2

    # Устанавливаем сетку для графиков
    if num_plots == 2:
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))  # Сетка 1x2
    elif num_plots == 4:
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))  # Сетка 2x2
    else:
        raise ValueError("Должен быть как минимум один набор данных для отображения.")

    # Упрощаем работу с одним или двумя наборами осей
    if num_plots == 2:
        axs = [axs]

    # Функция для рисования эмпирической функции распределения
    def draw_empirical_cdf(data, ax):
        # Преобразуем строковые значения в числа
        not_nested_data = [float(value) for value in data[0]]
        hist, edges = np.histogram(not_nested_data, bins=len(not_nested_data))
        Y = hist.cumsum() / hist.sum()

        # Линия для 0.0 слева от минимального значения
        ax.plot([min(not_nested_data) - 7, min(not_nested_data)], [0.0, 0.0], c="blue")
        for i in range(len(Y)):
            ax.plot([edges[i], edges[i + 1]], [Y[i], Y[i]], c="blue")

        # Линия для 1.0 справа от максимального значения
        ax.plot([max(not_nested_data), max(not_nested_data) + 7], [Y[-1], Y[-1]], c="blue")

        # Динамически определяем сетку
        size = len(not_nested_data) / 10
        if size >= 10:
            n = 10
        elif 5 < size < 10:
            n = 5
        else:
            n = 2

        ax.set_title("Эмпирическая функция распределения")
        ax.set_xlabel("Значения случайной величины, X")
        ax.set_ylabel("Fn(X)")
        ax.set_xticks(np.arange(min(not_nested_data), max(not_nested_data) + n, n))  # Деления по оси X каждые n
        ax.set_yticks(np.arange(0.0, 1.1, 0.1))
        ax.grid(True)

    # Функция для рисования гистограммы
    def draw_histogram(intervals, ax):
        x_labels = [t[0] for t in intervals[:-1]]  # Все интервалы, кроме последнего (Сумма)
        heights = [t[1] for t in intervals[:-1]]  # Количество для всех интервалов, кроме последнего

        ax.bar(x_labels, heights, width=0.5, align='center')
        ax.set_xlabel('Интервалы')
        ax.set_ylabel('Частота')
        ax.set_title('Статистическая функция распределения')
        ax.set_xticks(x_labels)
        ax.set_xticklabels(x_labels, rotation=45, ha='right')

    plot_idx = 0  # Индекс для отслеживания текущего графика

    # Рисуем графики для первого набора данных, если он есть
    if data1 is not None and intervals1 is not None:
        draw_empirical_cdf(data1, axs[plot_idx // 2][plot_idx % 2])
        plot_idx += 1
        draw_histogram(intervals1, axs[plot_idx // 2][plot_idx % 2])
        plot_idx += 1

    # Рисуем графики для второго набора данных, если он есть
    if data2 is not None and intervals2 is not None:
        draw_empirical_cdf(data2, axs[plot_idx // 2][plot_idx % 2])
        plot_idx += 1
        draw_histogram(intervals2, axs[plot_idx // 2][plot_idx % 2])
        plot_idx += 1

    plt.tight_layout()  # Подгоняем размещение графиков и меток
    plt.show()
