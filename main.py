import os
import tkinter as tk
from datetime import datetime
from functions import *

# Создаем основное окно
root = tk.Tk()

manual_data = []  # Глобальный список данных ручного ввода
random_data = []  # Глобальный список данных случайной генерации
manual_intervals_with_frequencies = []  # Глобальный список интервалов с частотами для ручного ввода
random_intervals_with_frequencies = []  # Глобальный список интервалов с частотами для случайной генерации

root.title("Математическое моделирование, лабораторная работа №1")

# region Обработчики для кнопок

# region Переключение экрана

# Переменная для хранения состояния полноэкранного режима
full_screen = False


# Функция для переключения полноэкранного режима
def toggle_full_screen(event=None):
    global full_screen
    if full_screen:
        root.attributes("-fullscreen", False)
        full_screen = False
    else:
        root.attributes("-fullscreen", True)
        full_screen = True


# Обработчик для выхода из полноэкранного режима (по клавише Esc)
root.bind("<Escape>", toggle_full_screen)

# Устанавливаем окно в полноэкранный режим при запуске
toggle_full_screen()


# endregion

# def display_data(data, name_of_display, name_of_file):
#
#     formatted_values = []
#     for item in data:
#         index = item[0]  # Первый элемент кортежа
#         value = item[1]  # Второй элемент кортежа
#         # Форматируем значение
#         formatted_value = f"({index}, {value:.2f})"
#         formatted_values.append(formatted_value)
#
#     # Проверяем, есть ли уже текст в поле
#     name_of_display.config(state="normal")  # Включаем возможность записи
#
#     if name_of_display.get("1.0", tk.END).strip():  # Если в текстовом поле уже есть текст
#         name_of_display.insert(tk.END, ", ")  # Добавляем запятую перед новыми значениями
#
#     # Записываем отформатированные значения в текстовое поле
#     name_of_display.insert(tk.END, ", ".join(formatted_values))  # Добавляем все отформатированные значения
#     name_of_display.config(state="disabled")  # Запрещаем редактирование снова
#
#     # Записываем данные в файл
#     with open(name_of_file, 'a', encoding='utf-8') as file:
#         file.write(", ".join(formatted_values) + "\n")

def clear_text(name_of_textfield):
    """
    Функция для удаления значений из поля текста
    :param name_of_textfield: имя переменной виджета, в котором удаляется текст
    :return:
    """
    name_of_textfield.config(state="normal")  # Включаем возможность записи
    name_of_textfield.delete("1.0", tk.END)  # Очищаем текстовое поле
    name_of_textfield.config(state="disabled")  # Запрещаем редактирование снова


def add_text(name_of_textfield, text):
    """
    Функция для записи текста в поле текста
    :param name_of_textfield: имя переменной виджета, в который добавляется запись
    :param text: текст записи
    :return:
    """
    name_of_textfield.config(state="normal")  # Включаем возможность записи
    name_of_textfield.insert(tk.END, text)  # Добавляем текст в поле
    name_of_textfield.config(state="disabled")  # Запрещаем редактирование снова


def set_entry_value(name_of_entry, value):
    """
    Функция для очистки и установления значения по умолчанию в поле Entry
    :param name_of_entry: имя переменной виджета, с которым проводятся действия
    :param value: значение, записываемое в виджет
    :return:
    """

    def clear_entry():
        """
        Функция для очистки поля Entry
        :return:
        """
        name_of_entry.delete(0, tk.END)

    clear_entry()  # Очистка
    name_of_entry.insert(0, value)  # Запись


def save_in_file(name_of_file: str, result_data: [(int, float)]):
    """
    Функция для сохранения данных в файл
    :param name_of_file: Имя .txt файла без указания расширения
    :param result_data: данные для записи в файл
    :return:
    """
    try:
        # Даем файлу расширение .txt
        name_of_file = name_of_file + ".txt"

        current_datetime = datetime.now()  # получение текущего времени

        # Запись данных в файл
        with open(name_of_file, 'a', encoding='utf-8') as file:
            # Проверка на наличие записей в файл для корректной записи данных
            if os.stat(name_of_file).st_size == 0:
                file.write(f"Запись от {current_datetime}. \n")
            else:
                file.write(f"\nЗапись от {current_datetime}.\n")

            # Записывание данных без индекса
            for i in range(len(result_data)):
                if i != len(result_data) - 1:
                    file.write(f"{result_data[i][1]}, ")
                else:
                    file.write(f"{result_data[i][1]}")

    except ValueError:
        print("Не удалось сохранить запись в файл!")
    finally:
        file.close()


def display_data(name_of_display, is_random=False, data=[]):
    """
    Отображает данные в текстовом поле и записывает их в файл.
    :param name_of_display: Имя переменной дисплея, в которое записываются значения
    :param is_random: Переменная для выбора режима отображения: True - для генерации, False - для ручного ввода
    :param data: Список с данными (для генерации, В РУЧНОМ РЕЖИМЕ НЕ УКАЗЫВАТЬ)
    :return:
    """
    formatted_values = []  # Список с отформатированными значениями
    result_data = []  # Список с итоговым результатом

    if is_random:  # Для случайной генерации
        # Обработка сгенерированных данных (список кортежей)
        for item in data:
            value = item[1]  # Второй элемент кортежа
            formatted_value = f"{value:.2f}"  # Форматируем значение
            formatted_values.append(formatted_value)

    else:
        # Для ручного ввода
        value = manual_entry.get()  # Получаем текст из поля ввода
        if value:  # Если значение не пустое
            # Заменяем запятую на точку
            value = value.replace(",", ".")

            # Разделяем строку на числа, используя `;` в качестве разделителя
            number_strings = value.split(';')
            formatted_values = []

            for num_str in number_strings:
                num_str = num_str.strip()  # Удаляем лишние пробелы
                if num_str:  # Проверяем, что строка не пустая
                    num_value = float(num_str)  # Преобразуем значение в число с плавающей точкой
                    formatted_value = f"{num_value:.2f}"  # Форматируем число
                    formatted_values.append(formatted_value)  # Добавляем отформатированное значение в список

    # Отображение данных в текстовом поле
    name_of_display.config(state="normal")  # Включаем возможность записи

    if name_of_display.get("1.0", tk.END).strip():  # Если текстовое поле не пустое
        name_of_display.insert(tk.END, ", ")  # Добавляем запятую перед новыми значениями

    name_of_display.insert(tk.END, ", ".join(formatted_values))  # Добавляем отформатированные значения
    name_of_display.config(state="disabled")  # Запрещаем редактирование снова

    if not is_random:
        # Очищаем поле ввода и возвращаем фокус
        manual_entry.delete(0, tk.END)  # Очищаем поле ввода
        manual_entry.focus_set()  # Устанавливаем фокус на поле ввода

    # Сохранение данных в результирующий список
    result_data.append(formatted_values)

    return result_data


def add_value(event=None):
    """
    Ручное добавление значений
    :param event:
    :return:
    """
    global manual_data  # Ищем глобальный список с данными
    # Сохраняем в этот список добавленные значения
    manual_data = display_data(manual_values_display, False)


def manual_calculation(event=None):
    """
    Расчет необходимых значений для данных ручного ввода
    :param event:
    :return:
    """
    try:
        global manual_intervals_with_frequencies
        # очищаем поля, чтобы в них ничего не было от прошлых записей
        clear_text(dispersion_manual_text)
        clear_text(sample_mean_manual_text)

        sorted_manual_data = list()  # Создаем список отформатированных значений
        count = 1  # Порядковый номер записи
        minimum = float(manual_data[0][0])  # Для поиска минимального значения в выборке

        # Переводим все числа из str во float
        for i in range(len(manual_data)):
            for j in range(len(manual_data[i])):
                sorted_manual_data.append((count, float(manual_data[i][j])))
                count += 1
                # Параллельно ищем минимальное значение
                if float(manual_data[i][j]) < minimum:
                    minimum = float(manual_data[i][j])

        sample_mean = get_sample_mean(sorted_manual_data)  # Выборочная средняя
        standard_deviation = get_standard_deviation(sorted_manual_data, sample_mean)  # Среднеквадратичное отклонение
        dispersion = get_dispersion(standard_deviation)  # Дисперсия
        n = get_the_number_of_intervals_using_the_Sturgess_formula(
            len(sorted_manual_data))  # Количество интервалов по формуле Стурджесса
        R = get_sample_size(sorted_manual_data)  # Размах
        delta_x = get_size_of_the_intervals(R, n)  # Размер интервала
        manual_intervals_with_frequencies = get_intervals_with_frequency_distribution(minimum, n, delta_x,
                                                                                      sorted_manual_data)  # Получившиеся интервалы с частотным распределением

        save_in_file("manual_generate", sorted_manual_data)  # Сохранение исходных полученных данных в файл

        # Отображение результатов в интерфейсе
        add_text(dispersion_manual_text, dispersion)
        add_text(sample_mean_manual_text, sample_mean)

    except IndexError:
        print("Нет выборки")


def random_generate(event=None):
    """
    Случайная генерация значений
    :param event:
    :return:
    """
    global random_data

    # Очищаем поле вывода перед генерацией новых данных
    clear_text(random_values_display)
    # Обнуляем данные случайной генерации
    random_data = []

    try:
        # Проверяем фиксацию сида
        if seed_fixation.get() == 1:
            random_seed = True
        else:
            random_seed = False

        # Проверяем фиксацию типа чисел
        if int_fixation.get() == 1:
            type_of_numbers = True
        else:
            type_of_numbers = False

        N = int(size_of_data_entry.get())  # размер выборки данных
        minimal_value = float(min_value_entry.get())  # минимальные значения генерации
        maximal_value = float(max_value_entry.get())  # максимальные значения генерации

        # Генерация данных
        random_generated_data = generate_data(N, minimal_value, maximal_value, random_seed, type_of_numbers)

        # Сохранение сгенерированных данных и отображение их в интерфейсе
        random_data = display_data(random_values_display, True, random_generated_data)

    except ValueError:
        print("Ошибка!")


def random_calculation(event=None):
    try:
        global random_intervals_with_frequencies

        # Очищаем поля вывода информации
        clear_text(dispersion_random_text)
        clear_text(sample_mean_random_text)

        sorted_random_data = list()  # Список форматированных данных
        count = 1  # переменная счетчика индекса
        minimum = float(random_data[0][0])  # переменная для нахождения минимального значения в выборке данных
        for i in range(len(random_data)):
            for j in range(len(random_data[i])):
                sorted_random_data.append((count, float(random_data[i][j])))
                count += 1
                if float(random_data[i][j]) < minimum:
                    minimum = float(random_data[i][j])

        random_sample_mean = get_sample_mean(sorted_random_data)  # Выборочная средняя
        random_standard_deviation = get_standard_deviation(sorted_random_data,
                                                           random_sample_mean)  # Среднеквадратичное отклонение
        random_dispersion = get_dispersion(random_standard_deviation)  # Дисперсия
        random_n = get_the_number_of_intervals_using_the_Sturgess_formula(
            len(sorted_random_data))  # Количество интервалов по формуле Стурджесса
        random_R = get_sample_size(sorted_random_data)  # Размах
        random_delta_x = get_size_of_the_intervals(random_R, random_n)  # Размер интервала
        random_intervals_with_frequencies = get_intervals_with_frequency_distribution(minimum, random_n, random_delta_x,
                                                                                      sorted_random_data)  # Получившиеся интервалы с частотным распределением

        save_in_file("random_generate", sorted_random_data)  # Сохранение исходных полученных данных в файл

        # Отображение результатов в интерфейсе
        add_text(dispersion_random_text, random_dispersion)
        add_text(sample_mean_random_text, random_sample_mean)

    except IndexError:
        print("Нет выборки случайной генерации")


def draw_graphics(event=None):
    """Функция для визуализации данных"""
    global manual_data, manual_intervals_with_frequencies, random_data, random_intervals_with_frequencies  # Получение глобальных данных

    # Проверяем данные, чтобы понять, сколько и какие графики отображать
    if not len(manual_data) > 0 and not len(
            manual_intervals_with_frequencies) > 0:  # Присутствуют данные только случайной генерации
        draw_combined_graphs(data2=random_data, intervals2=random_intervals_with_frequencies)
    if not len(random_data) > 0 and not len(
            random_intervals_with_frequencies) > 0:  # Присутствуют данные только ручного ввода
        draw_combined_graphs(data1=manual_data, intervals1=manual_intervals_with_frequencies)
    if (len(manual_data) > 0 and len(manual_intervals_with_frequencies) > 0) and (
            len(random_data) > 0 and len(random_intervals_with_frequencies) > 0):  # Отрисовка обоих наборов данных
        draw_combined_graphs(manual_data, manual_intervals_with_frequencies, random_data,
                             random_intervals_with_frequencies)


def clear_all(event=None):
    """
    Функция для сброса всех введенных пользователем данных к первоначальным
    :param event:
    :return:
    """
    global manual_data, random_data, manual_intervals_with_frequencies, random_intervals_with_frequencies

    # Очистка хранилищ
    manual_data, random_data, manual_intervals_with_frequencies, random_intervals_with_frequencies = [], [], [], []

    # region Поля ручного ввода
    set_entry_value(manual_entry, "")
    clear_text(manual_values_display)
    clear_text(dispersion_manual_text)
    clear_text(sample_mean_manual_text)
    # endregion

    # region  Поля случайной генерации
    set_entry_value(size_of_data_entry, "100")
    set_entry_value(min_value_entry, "18")
    set_entry_value(max_value_entry, "90")
    clear_text(random_values_display)

    # Сброс галочек
    if seed_fixation.get() == 1:
        seed_fixation.set(0)
    if int_fixation.get() == 1:
        int_fixation.set(0)

    clear_text(dispersion_random_text)
    clear_text(sample_mean_random_text)
    # endregion


def paste_from_clipboard(event=None):
    """
    Функция для вставки текста из буфера обмена
    :param event:
    :return:
    """
    try:
        # Получаем данные из буфера обмена
        clipboard_data = root.clipboard_get()

        # Вставляем данные в поле Entry
        manual_entry.insert(tk.INSERT, clipboard_data)
    except tk.TclError:
        print("Буфер обмена пустой!")


# endregion

# region Интерфейс
# Настраиваем сетку окна
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

# region Стандартные значения для виджетов
standard_height = 1  # высота виджета
standard_width = 40  # ширина виджета
font = ("Arial", 10)  # шрифт и его размер
padding = 2  # отступы
# endregion

# region Ручное заполнение
# поле отделения
manual_label = tk.Label(root, text="Ручное заполнение", height=int(standard_height * 1.5),
                        width=int(standard_width * 1.5),
                        font=font)
manual_label.grid(row=0, column=0, columnspan=5, sticky="ew")

# поле информации
manual_entry_text = tk.Label(root, text="Введите значения:", height=standard_height, width=standard_width, font=font,
                             padx=padding, pady=padding)
manual_entry_text.grid(row=1, column=0)

# поле ввода
manual_entry = tk.Entry(root, width=standard_width, font=font)
manual_entry.grid(row=1, column=1, padx=padding, pady=padding)
manual_entry.bind("<Return>", add_value)  # Добавление данных нажатием Enter
manual_entry.bind("<Shift-Return>", manual_calculation)  # Запуск расчета нажатием Shift + Enter
manual_entry.bind("<Control-v>", paste_from_clipboard)  # Возможность вставить текст из буфера обмена Ctrl + V
manual_entry.bind("<Shift-Insert>", paste_from_clipboard)  # Возможность вставить текст из буфера обмена Shift + Insert

# поле отображения
manual_values_display = tk.Text(root, height=standard_height, width=standard_width, font=font)
manual_values_display.grid(row=1, column=2, columnspan=2, padx=padding, pady=padding, sticky="ew")
manual_values_display.config(state="disabled")

# кнопка расчета
manual_draw_button = tk.Button(root, text="Рассчитать", height=standard_height, width=standard_width, font=font,
                               command=manual_calculation)
manual_draw_button.grid(row=1, column=4, padx=padding, pady=padding)

# endregion

# Сепаратор
separator_frame = tk.Frame(root, height=2, bg="grey")  # Высота линии 2px
separator_frame.grid(row=2, column=0, columnspan=5, sticky="ew", padx=5, pady=(5, 5))  # Растягиваем по ширине

# region Результаты расчетов ручного ввода
# поле отделения
result_manual_label = tk.Label(root, text="Результаты для ручного ввода", height=int(standard_height * 1.5),
                               width=int(standard_width * 1.5),
                               font=font)
result_manual_label.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky="ew")

# поле информации о минимальном значении выборки
sample_mean_manual_label = tk.Label(root, text="Выборочная средняя:", height=standard_height,
                                    width=standard_width,
                                    font=font,
                                    padx=padding, pady=padding)
sample_mean_manual_label.grid(row=4, column=0)

sample_mean_manual_text = tk.Text(root, height=standard_height, width=standard_width, font=font)
sample_mean_manual_text.grid(row=4, column=1)
sample_mean_manual_text.config(state="disabled")

dispersion_manual_label = tk.Label(root, text="Дисперсия:", height=standard_height,
                                   width=standard_width,
                                   font=font,
                                   padx=padding, pady=padding)
dispersion_manual_label.grid(row=4, column=3)

dispersion_manual_text = tk.Text(root, height=standard_height, width=standard_width, font=font)
dispersion_manual_text.grid(row=4, column=4)
dispersion_manual_text.config(state="disabled")
# endregion

# Сепаратор
separator_frame2 = tk.Frame(root, height=2, bg="black")  # Высота линии 2px
separator_frame2.grid(row=5, column=0, columnspan=5, sticky="ew", padx=5, pady=(5, 5))  # Растягиваем по ширине

# region Случайная генерация
# поле отделения
random_label = tk.Label(root, text="Случайное заполнение", height=standard_height,
                        width=int(standard_width * 1.5),
                        font=font)
random_label.grid(row=6, column=0, columnspan=5, sticky="ew")

# поле информации о размере выборки
size_of_data_label = tk.Label(root, text="Введите размер выборки:", height=standard_height, width=standard_width,
                              font=font,
                              padx=padding, pady=padding)
size_of_data_label.grid(row=7, column=0)

# поле ввода размера выборки
size_of_data_entry = tk.Entry(root, width=standard_width, font=font)
size_of_data_entry.grid(row=7, column=1, padx=padding, pady=padding)
size_of_data_entry.insert(tk.END, "100")

# поле информации о минимальном значении выборки
min_value_label = tk.Label(root, text="Введите минимальное значение выборки:", height=standard_height,
                           width=standard_width,
                           font=font,
                           padx=padding, pady=padding)
min_value_label.grid(row=8, column=0)

# поле ввода минимального значения выборки
min_value_entry = tk.Entry(root, width=standard_width, font=font)
min_value_entry.grid(row=8, column=1, padx=padding, pady=padding)
min_value_entry.insert(tk.END, "18")

# поле информации о максимальном значении выборки
max_value_label = tk.Label(root, text="Введите минимальное значение выборки:", height=standard_height,
                           width=standard_width,
                           font=font,
                           padx=padding, pady=padding)
max_value_label.grid(row=9, column=0)

# поле ввода максимального значения выборки
max_value_entry = tk.Entry(root, width=standard_width, font=font)
max_value_entry.grid(row=9, column=1, padx=padding, pady=padding)
max_value_entry.insert(tk.END, "90")

# кнопка фиксации сида
seed_fixation = tk.IntVar()
checkbutton = tk.Checkbutton(root, text="Фиксация сида", variable=seed_fixation, height=standard_height,
                             width=standard_width, font=font)
checkbutton.grid(row=10, column=0, padx=padding, pady=padding)

# кнопка фиксации целых чисел
int_fixation = tk.IntVar()
checkbutton = tk.Checkbutton(root, text="Генерировать только целый числа", variable=int_fixation,
                             height=standard_height,
                             width=standard_width, font=font)
checkbutton.grid(row=10, column=1, padx=padding, pady=padding)

# кнопка генерации случайных значений
random_generate_button = tk.Button(root, text="Сгенерировать", height=standard_height, width=standard_width, font=font,
                                   command=random_generate)
random_generate_button.grid(row=7, rowspan=4, column=2, padx=padding, pady=padding, sticky="ns")

# поле отображения
random_values_display = tk.Text(root, height=standard_height, width=standard_width, font=font)
random_values_display.grid(row=7, rowspan=4, column=3, padx=padding, pady=padding, sticky="ns")
random_values_display.config(state="disabled")

# кнопка расчета случайных данных
random_draw_button = tk.Button(root, text="Рассчитать", height=standard_height, width=standard_width, font=font,
                               command=random_calculation)
random_draw_button.grid(row=7, rowspan=4, column=4, padx=padding, pady=padding, sticky="ns")

# endregion

# Сепаратор
separator_frame3 = tk.Frame(root, height=2, bg="grey")  # Высота линии 2px
separator_frame3.grid(row=11, column=0, columnspan=5, sticky="ew", padx=5, pady=(5, 5))  # Растягиваем по ширине

# region Результаты расчетов генерации
# поле отделения
result_label = tk.Label(root, text="Результаты для генерации", height=int(standard_height * 1.5),
                        width=int(standard_width * 1.5),
                        font=font)
result_label.grid(row=12, column=0, columnspan=5, padx=5, pady=5, sticky="ew")

# поле информации о минимальном значении выборки
sample_mean_random_label = tk.Label(root, text="Выборочная средняя:", height=standard_height,
                                    width=standard_width,
                                    font=font,
                                    padx=padding, pady=padding)
sample_mean_random_label.grid(row=13, column=0)

sample_mean_random_text = tk.Text(root, height=standard_height, width=standard_width, font=font)
sample_mean_random_text.grid(row=13, column=1)

dispersion_random_label = tk.Label(root, text="Дисперсия:", height=standard_height,
                                   width=standard_width,
                                   font=font,
                                   padx=padding, pady=padding)
dispersion_random_label.grid(row=13, column=3)

dispersion_random_text = tk.Text(root, height=standard_height, width=standard_width, font=font)
dispersion_random_text.grid(row=13, column=4)
# endregion

# Сепаратор
separator_frame4 = tk.Frame(root, height=2, bg="black")  # Высота линии 2px
separator_frame4.grid(row=14, column=0, columnspan=5, sticky="ew", padx=5, pady=(5, 5))  # Растягиваем по ширине

# region Кнопки
draw_graphics_btn = tk.Button(root, text="Перейти к графикам", height=standard_height, width=standard_width, font=font,
                              command=draw_graphics)
draw_graphics_btn.grid(row=15, column=2, columnspan=3, padx=padding, pady=padding, sticky="ew")

clear_all_btn = tk.Button(root, text="Сбросить все", height=standard_height, width=standard_width, font=font,
                          command=clear_all)
clear_all_btn.grid(row=15, column=0, columnspan=2, padx=padding, pady=padding, sticky="ew")
# endregion
# endregion

# Запуск главного цикла обработки событий
root.mainloop()
