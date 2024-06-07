from tkinter import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from wav_audio.audioWav import AudiofileWav
from front.dialog_window import TrimDialog
from mp3_audio.audioMP3 import AudiofileMP3
from front.file_helper import FileManager
from front.basic_functions_gui import BasicFunctions
from front.equalizer import Equalizer
from back.help_functions import (open_file_dialog, draw_plot_back,
                                 plot_mp3_file_back, plot_wav_file_back,
                                 parse_file, find_template_info)
from back.paths import path_user_data


class WindowAudio:
    """Окно с аудио проектом"""

    def __init__(self, window, version_handler, path, name):
        """Инициация стартового окна"""
        self.arr_buttons = None
        self.window = window
        self.time = 0
        self.audio = None
        self.path = None
        self.temp_path = path
        self.name_project = name
        self.format = ''
        self.version_handler = version_handler
        self.label = None
        self.window_helper = BasicFunctions()
        self.mp3_format = '.mp3'
        self.wav_format = '.wav'

    def open_exist_project(self):
        """Открытие уже созданного проекта"""
        audio_window = self.make_standard_window()
        if self.execute_project_mp3(audio_window) == -1:
            self.execute_project_wav(audio_window)
        f = open((path_user_data +
                  self.name_project + "/versions.txt"), 'w')
        f.close()
        self.place_buttons(audio_window)

    def execute_project_mp3(self, audio_window):
        """Обработка mp3 проекта при повторном открытии"""
        try:
            open(self.temp_path + '.mp3', 'r')
            self.temp_path += '.mp3'
            self.version_handler.first_path = \
                (path_user_data + self.name_project + "/first.mp3")
            self.version_handler.format = 'mp3'
            self.format = 'mp3'
            self.audio = AudiofileMP3(self.temp_path)
            self.plot_mp3_file(audio_window, self.temp_path)
        except FileNotFoundError:
            return -1

    def execute_project_wav(self, audio_window):
        """Обработка wav проекта при повторном открытии"""
        self.temp_path += self.wav_format
        self.version_handler.first_path = \
            (path_user_data +
             self.name_project + "/first.wav")
        self.version_handler.format = 'wav'
        self.format = 'wav'
        self.audio = AudiofileWav(self.temp_path)
        self.plot_wav_file(audio_window)

    def make_standard_window(self):
        """Создания стандартного окна с аудио"""
        self.window.withdraw()
        audio_window = self.window_helper.standard_window(self.name_project,
                                                          "1400x900")
        return audio_window

    def place_buttons(self, audio_window):
        """Размещение виджетов на окне с аудио"""
        (button_split, button_erase, button_speed, button_back, button_next,
         button_save, button_exit, button_template,
         button_equalizer) = self.place_all_buttons(
            audio_window)
        self.arr_buttons = [button_erase, button_speed, button_back,
                            button_next,
                            button_save, button_exit, button_template,
                            button_equalizer]
        self.place_time_audio(window=audio_window)
        self.check_activity_buttons()
        self.set_button_functions(button_split, audio_window)

    def make_audio_window(self):
        """Создание окна с аудио"""
        audio_window = self.make_standard_window()
        self.place_buttons(audio_window)

    def set_button_functions(self, button_split, window):
        """Установка функций управляющим кнопкам"""
        button_split.bind("<Button-1>", lambda e: self.function_button_split(
            e, window))
        self.arr_buttons[0].bind("<Button-1>", lambda e: self.
                                 function_button_erase(e, window))
        self.arr_buttons[1].bind("<Button-1>", lambda e: self.
                                 function_button_speed(e, window))
        self.arr_buttons[4].bind("<Button-1>", self.function_button_save)
        self.arr_buttons[2].bind("<Button-1>", lambda e: self.
                                 function_button_back(e, window))
        self.arr_buttons[3].bind("<Button-1>", lambda e: self.
                                 function_button_next(e, window))
        self.arr_buttons[5].bind("<Button-1>", lambda e: self.
                                 function_button_exit(e, window))
        self.arr_buttons[6].bind("<Button-1>", lambda e: self.
                                 function_button_template(e, window))
        self.arr_buttons[7].bind("<Button-1>", lambda e: self.
                                 function_button_equalizer(e, window))

    def check_activity_buttons(self):
        """Проверка на активность кнопок"""
        if self.time == 0:
            for button in self.arr_buttons:
                button.configure(state=DISABLED)
        else:
            for button in self.arr_buttons:
                button.configure(state=NORMAL)
            if not self.version_handler.check_back_activity():
                self.arr_buttons[2].configure(state=DISABLED)
            if not self.version_handler.check_next_activity():
                self.arr_buttons[3].configure(state=DISABLED)

    def place_all_buttons(self, audio_window):
        """Создание управляющих кнопок"""
        button_split = self.window_helper.return_standard_button("Вставить",
                                                                 audio_window,
                                                                 15, 5)
        button_erase = self.window_helper.return_standard_button("Обрезать",
                                                                 audio_window,
                                                                 15, 5)
        button_speed = self.window_helper.return_standard_button("Скорость",
                                                                 audio_window,
                                                                 15, 5)
        button_back = self.window_helper.return_standard_button("Назад",
                                                                audio_window,
                                                                15, 5)
        button_next = self.window_helper.return_standard_button("Вперед",
                                                                audio_window,
                                                                15, 5)
        button_save = self.window_helper.return_standard_button("Сохранить",
                                                                audio_window,
                                                                15, 5)
        button_exit = self.window_helper.return_standard_button("Выйти",
                                                                audio_window,
                                                                15, 5)
        button_temp = self.window_helper.return_standard_button("Шаблоны",
                                                                audio_window,
                                                                15, 5)
        button_equalizer = self.window_helper.return_standard_button(
            "Эквалайзер",
            audio_window,
            15, 5)
        button_split.place(x=10, y=20)
        button_erase.place(x=190, y=20)
        button_speed.place(x=370, y=20)
        button_next.place(x=550, y=20)
        button_back.place(x=730, y=20)
        button_temp.place(x=910, y=20)
        button_equalizer.place(x=1090, y=20)
        button_save.place(x=850, y=650)
        button_exit.place(x=1130, y=650)
        return (button_split, button_erase, button_speed, button_back,
                button_next, button_save, button_exit, button_temp,
                button_equalizer)

    def draw_plot(self, window, times, signal_array):
        """Рисование графика"""
        figure = draw_plot_back(times, signal_array)
        canvas_plot = FigureCanvasTkAgg(figure, window)
        canvas_plot.draw()
        label = Label(window, text="", width=20)
        canvas_plot.get_tk_widget().place(x=10, y=150)

        def update_coordinates(event=None):
            try:
                x, y = event.x, event.y
                label.place(x=x + 10, y=y + 150)
                x, y = self.count_coordinates(x, y)
                label.config(text="X: {}, Y: {}".format(x, y))
                window.after(500,
                             update_coordinates)
            except AttributeError:
                pass

        canvas_plot.get_tk_widget().bind('<Motion>', update_coordinates)

    def count_coordinates(self, x, y):

        canvas_width = 780
        canvas_height = 300

        time_per_pixel = self.time / canvas_width
        x_coord = int(x * time_per_pixel)

        amplitude_per_pixel = 30000 / canvas_height
        y_coord = 15000 - (
                    y * amplitude_per_pixel)

        return x_coord, y_coord

    def plot_mp3_file(self, window, path):
        """Вычисление данных для рисования графика MP3"""
        times, data, duration = plot_mp3_file_back(path)
        self.draw_plot(window, times, data)
        self.time = int(duration)

    def plot_wav_file(self, window):
        """Вычисление данных для рисования графика WAV"""
        times, signal_array = plot_wav_file_back(self.audio)
        self.draw_plot(window, times, signal_array)
        self.time = int(self.audio.stHeaderFields.size_sec)

    def place_time_audio(self, window):
        """Размещение отметки времени"""
        time_text = str(self.time) + " seconds"
        self.label = Label(window, text=time_text, font=("Arial", 30))
        self.label.place(x=100, y=650)

    def first_split(self, window):
        """Вставка первого куска аудио"""
        path = open_file_dialog()
        self.path = path
        if self.path.endswith(self.mp3_format):
            self.format = 'mp3'
            self.audio = AudiofileMP3(self.path)
            self.plot_mp3_file(window, self.path)
            self.audio.output_files(self.temp_path + '.' + self.format)
        else:
            self.format = 'wav'
            self.audio = AudiofileWav(self.path)
            self.plot_wav_file(window)
            self.temp_path += self.wav_format
            self.audio.output_files(self.temp_path)
        self.version_handler.output_first_version(self.audio, self.format)

    def function_button_split(self, event, window):
        """Функция вставки"""
        if self.time == 0:
            self.first_split(window)
        else:
            path = open_file_dialog(self.format)
            dialog = TrimDialog(window, "Вставка", 'split')
            start = dialog.start
            self.spliting_audio(path, window, start)
        temp_time = str(self.time) + ' seconds'
        self.label.configure(text=temp_time)
        self.check_activity_buttons()

    def spliting_audio(self, path, window, start):
        if self.format == 'mp3':
            other = AudiofileMP3(path)
        else:
            other = AudiofileWav(path)
        self.audio.splice_audio(self.temp_path, other, start)
        if self.format == 'mp3':
            self.plot_mp3_file(window, self.temp_path + self.mp3_format)
        else:
            self.plot_wav_file(window)
        self.version_handler.write_changes('split', path_split=path,
                                           start=start)

    def function_button_erase(self, event, window):
        """Функция обрезки"""
        dialog = TrimDialog(window, "Обрезка", 'erase')
        start = dialog.start
        end = dialog.end
        self.erasing_audio(start, end, window)

    def erasing_audio(self, start, end, window):
        self.audio.crop_audio(self.temp_path, start, end)
        if self.format == 'mp3':
            self.plot_mp3_file(window, self.temp_path + self.mp3_format)
        else:
            self.plot_wav_file(window)
        self.version_handler.write_changes('erase', start=start, end=end)
        temp_time = str(self.time) + ' seconds'
        self.label.configure(text=temp_time)
        self.check_activity_buttons()

    def function_button_speed(self, event, window):
        """Функция изменения скорости"""
        dialog = TrimDialog(window, "Изменение скорости", 'speed')
        speed = dialog.start
        self.speeding_audio(window, speed)

    def speeding_audio(self, window, speed):
        if self.format == 'mp3':
            self.audio.speed_up_audio(self.temp_path + self.mp3_format, speed)
            self.plot_mp3_file(window, self.temp_path + self.mp3_format)
        else:
            self.audio.speed_up_audio(self.temp_path, speed)
            self.plot_wav_file(window)
        self.version_handler.write_changes('speed', speed=speed)
        temp_time = str(self.time) + ' seconds'
        self.label.configure(text=temp_time)
        self.check_activity_buttons()

    def function_button_save(self, event):
        """Функция сохранения"""
        file_help = FileManager()
        self.path = file_help.save_file_as('.' + self.format)
        self.audio.output_files(self.path)

    def function_button_back(self, event, window):
        """Функция отката изменений"""
        audio_temp = self.version_handler.back_changes()
        self.process_changes(audio_temp, window)

    def process_changes(self, audio_temp, window):
        """Функция обработки изменений"""
        self.audio = audio_temp
        if self.format == 'mp3':
            self.audio.output_files(self.temp_path + self.mp3_format)
            self.plot_mp3_file(window, self.temp_path + self.mp3_format)
        else:
            self.audio.output_files(self.temp_path)
            self.plot_wav_file(window)
        temp_time = str(self.time) + ' seconds'
        self.label.configure(text=temp_time)
        self.check_activity_buttons()

    def function_button_next(self, event, window):
        """Функция возвращения изменений"""
        audio_temp = self.version_handler.next_changes()
        self.process_changes(audio_temp, window)

    def function_button_exit(self, event, window):
        """Кнопка выхода"""
        window.destroy()
        self.window.deiconify()

    def function_button_template(self, event, window):
        """Функция возвращения изменений"""
        template_window = self.window_helper.standard_window('Шаблоны',
                                                             "400x300")
        button_new_template = self.window_helper.return_standard_button(
            'Добавить', template_window, 5, 3)
        button_new_template.bind("<Button-1>", lambda e: self.
                                 function_button_new_template(e,
                                                              template_window))

        button_new_template.pack(anchor='ne')
        templates, names = parse_file('templates.txt')
        for i in names:
            button = self.window_helper.return_standard_button(i,
                                                               template_window,
                                                               5, 3)
            button.bind("<Button-1>", lambda e, b=button: self.
                        execute_template(e, templates, b, window))
            button.pack(anchor="nw")

    def function_button_new_template(self, event, window):
        """Создание нового шаблона"""
        dialog_name = TrimDialog(window, "Название", 'name')
        name_project = dialog_name.start
        dialog = TrimDialog(window, "Обрезка", 'erase')
        erase_start = dialog.start
        erase_end = dialog.end
        path = open_file_dialog(self.format)
        split_start = None
        if path != '':
            dialog = TrimDialog(window, "Вставка", 'split')
            split_start = dialog.start
        else:
            path = None
        dialog = TrimDialog(window, "Скорость", 'speed')
        speed_count = dialog.start
        line = ''
        with (open('templates.txt', 'a+') as file):
            line += name_project + ' '
            line += str(erase_start) + ' ' + str(erase_end) + ' ' + str(
                path) + ' ' + str(split_start) + ' ' + str(speed_count) + '\n'
            file.write(line)

    def execute_template(self, event, templates, name_template, window):
        """Обработка шаблона"""
        info = find_template_info(templates, name_template['text'])
        if info['start_time'] is not None:
            start = float(info['start_time'])
            end = float(info['end_time'])
            self.erasing_audio(start, end, window)
        if info['insert_path'] is not None:
            path = info['insert_path']
            start = float(info['insert_time'])
            self.spliting_audio(path, window, start)
            temp_time = str(self.time) + ' seconds'
            self.label.configure(text=temp_time)
            self.check_activity_buttons()
        if info['speed'] is not None:
            speed = float(info['speed'])
            self.speeding_audio(window, speed)

    def function_button_equalizer(self, event, window):
        """Вызов эквалайзера"""
        equal = Equalizer(self.temp_path, self.format, window)
        equal.visualizing_equalizer()
        if self.format == 'mp3':
            self.audio.output_files(self.temp_path + self.mp3_format)
            self.plot_mp3_file(window, self.temp_path + self.mp3_format)
        else:
            self.audio.output_files(self.temp_path)
            self.plot_wav_file(window)
