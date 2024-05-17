from tkinter import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from wav_audio.audioWav import AudiofileWav
from front.dialog_window import TrimDialog
from mp3_audio.audioMP3 import AudiofileMP3
from front.file_helper import FileManager
from front.basic_functions_gui import BasicFunctions
from back.help_functions import (open_file_dialog, draw_plot_back,
                                 plot_mp3_file_back, plot_wav_file_back)
from back.paths import path_user_data


class WindowAudio:
    """Окно с аудио проектом"""
    def __init__(self, window, version_handler, path, name):
        """Инициация стартового окна"""
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
        self.temp_path += '.wav'
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
        audio_window = self.window_helper.standard_window(self.name_project)
        return audio_window

    def place_buttons(self, audio_window):
        """Размещение виджетов на окне с аудио"""
        (button_split, button_erase, button_speed, button_back, button_next,
         button_save, button_exit) = self.place_all_buttons(
            audio_window)
        arr_buttons = [button_erase, button_speed, button_back, button_next,
                       button_save, button_exit]
        self.place_time_audio(window=audio_window)
        self.check_activity_buttons(arr_buttons)
        self.set_button_functions(arr_buttons, button_split, audio_window)

    def make_audio_window(self):
        """Создание окна с аудио"""
        audio_window = self.make_standard_window()
        self.place_buttons(audio_window)

    def set_button_functions(self, arr_buttons, button_split, window):
        """Установка функций управляющим кнопкам"""
        button_split.bind("<Button-1>", lambda e: self.function_button_split(
            e, window, arr_buttons))
        arr_buttons[0].bind("<Button-1>", lambda e: self.
                            function_button_erase(e, window, arr_buttons))
        arr_buttons[1].bind("<Button-1>", lambda e: self.
                            function_button_speed(e, window, arr_buttons))
        arr_buttons[4].bind("<Button-1>", self.function_button_save)
        arr_buttons[2].bind("<Button-1>", lambda e: self.
                            function_button_back(e, window, arr_buttons))
        arr_buttons[3].bind("<Button-1>", lambda e: self.
                            function_button_next(e, window, arr_buttons))
        arr_buttons[5].bind("<Button-1>", lambda e: self.
                            function_button_exit(e, window))

    def check_activity_buttons(self, arr_buttons):
        """Проверка на активность кнопок"""
        if self.time == 0:
            for button in arr_buttons:
                button.configure(state=DISABLED)
        else:
            for button in arr_buttons:
                button.configure(state=NORMAL)
            if not self.version_handler.check_back_activity():
                arr_buttons[2].configure(state=DISABLED)
            if not self.version_handler.check_next_activity():
                arr_buttons[3].configure(state=DISABLED)

    def place_all_buttons(self, audio_window):
        """Создание управляющих кнопок"""
        button_split = self.window_helper.return_standard_button("Вставить",
                                                                 audio_window)
        button_erase = self.window_helper.return_standard_button("Обрезать",
                                                                 audio_window)
        button_speed = self.window_helper.return_standard_button("Скорость",
                                                                 audio_window)
        button_back = self.window_helper.return_standard_button("Назад",
                                                                audio_window)
        button_next = self.window_helper.return_standard_button("Вперед",
                                                                audio_window)
        button_save = self.window_helper.return_standard_button("Сохранить",
                                                                audio_window)
        button_exit = self.window_helper.return_standard_button("Выйти",
                                                                audio_window)
        button_split.place(x=10, y=20)
        button_erase.place(x=290, y=20)
        button_speed.place(x=570, y=20)
        button_next.place(x=850, y=20)
        button_back.place(x=1130, y=20)
        button_save.place(x=850, y=650)
        button_exit.place(x=1130, y=650)
        return (button_split, button_erase, button_speed, button_back,
                button_next, button_save, button_exit)

    @staticmethod
    def draw_plot(window, times, signal_array):
        """Рисование графика"""
        figure = draw_plot_back(times, signal_array)
        canvas = FigureCanvasTkAgg(figure, window)
        canvas.draw()
        canvas.get_tk_widget().place(x=10, y=150)

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
        if self.path.endswith('.mp3'):
            self.format = 'mp3'
            self.audio = AudiofileMP3(self.path)
            self.plot_mp3_file(window, self.path)
        else:
            self.format = 'wav'
            self.audio = AudiofileWav(self.path)
            self.plot_wav_file(window)
        self.audio.output_files(self.temp_path + '.' + self.format)
        self.version_handler.output_first_version(self.audio, self.format)

    def function_button_split(self, event, window, arr_buttons):
        """Функция вставки"""
        if self.time == 0:
            self.first_split(window)
        else:
            path = open_file_dialog(self.format)
            dialog = TrimDialog(window, "Вставка", 'split')
            if self.format == 'mp3':
                other = AudiofileMP3(path)
            else:
                other = AudiofileWav(path)
            start = dialog.start
            self.audio.splice_audio(self.temp_path, other, start)
            if self.format == 'mp3':
                self.plot_mp3_file(window, self.temp_path + '.mp3')
            else:
                self.plot_wav_file(window)
            self.version_handler.write_changes('split', path_split=path,
                                               start=start)
        temp_time = str(self.time) + ' seconds'
        self.label.configure(text=temp_time)
        self.check_activity_buttons(arr_buttons)

    def function_button_erase(self, event, window, arr_buttons):
        """Функция обрезки"""
        dialog = TrimDialog(window, "Обрезка", 'erase')
        start = dialog.start
        end = dialog.end
        self.audio.crop_audio(self.temp_path, start, end)
        if self.format == 'mp3':
            self.plot_mp3_file(window, self.temp_path + '.mp3')
        else:
            self.plot_wav_file(window)
        self.version_handler.write_changes('erase', start=start, end=end)
        temp_time = str(self.time) + ' seconds'
        self.label.configure(text=temp_time)
        self.check_activity_buttons(arr_buttons)

    def function_button_speed(self, event, window, arr_buttons):
        """Функция изменения скорости"""
        dialog = TrimDialog(window, "Изменение скорости", 'speed')
        speed = dialog.start
        if self.format == 'mp3':
            self.audio.speed_up_audio(self.temp_path + '.mp3', speed)
            self.plot_mp3_file(window, self.temp_path + '.mp3')
        else:
            self.audio.speed_up_audio(self.temp_path, speed)
            self.plot_wav_file(window)
        self.version_handler.write_changes('speed', speed=speed)
        temp_time = str(self.time) + ' seconds'
        self.label.configure(text=temp_time)
        self.check_activity_buttons(arr_buttons)

    def function_button_save(self, event):
        """Функция сохранения"""
        file_help = FileManager()
        self.path = file_help.save_file_as('.' + self.format)
        self.audio.output_files(self.path)

    def function_button_back(self, event, window, arr_buttons):
        """Функция отката изменений"""
        audio_temp = self.version_handler.back_changes()
        self.process_changes(audio_temp, window, arr_buttons)

    def process_changes(self, audio_temp, window, arr_buttons):
        """Функция обработки изменений"""
        self.audio = audio_temp
        if self.format == 'mp3':
            self.audio.output_files(self.temp_path + '.mp3')
            self.plot_mp3_file(window, self.temp_path + '.mp3')
        else:
            self.audio.output_files(self.temp_path + '.wav')
            self.plot_wav_file(window)
        temp_time = str(self.time) + ' seconds'
        self.label.configure(text=temp_time)
        self.check_activity_buttons(arr_buttons)

    def function_button_next(self, event, window, arr_buttons):
        """Функция возвращения изменений"""
        audio_temp = self.version_handler.next_changes()
        self.process_changes(audio_temp, window, arr_buttons)

    def function_button_exit(self, event, window):
        window.destroy()
        self.window.deiconify()
