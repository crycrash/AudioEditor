from tkinter import simpledialog, filedialog
from tkinter import *

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pydub import AudioSegment

from audioWav import AudiofileWav
from dialog_window import TrimDialog
from audioMP3 import AudiofileMP3
from file_helper import FileManager


class GUI:
    def __init__(self):
        """Инициация стартового окна"""
        self.window = Tk()
        self.time = 0
        self.audio = None
        self.path = None
        self.temp_path = ''
        self.name_project = ''
        self.format = ''

    def start_window(self):
        """Отображение стартового окна и кнопок"""
        self.window.title("Привет!")
        name_window = Label(self.window, text="Аудио редактор",
                            fg="white", font=("Arial Bold", 50), bg="blue")
        name_window.pack(anchor=N)
        self.window.geometry("1400x900")
        self.window.configure(background="blue")
        self.start_buttons()
        self.window.mainloop()

    @staticmethod
    def return_standard_button(text, window):
        """Cоздание базовой кнопки"""
        button = Button(window,
                        text=text,
                        width=15, height=5,
                        bg='white', fg="black"
                        )
        return button

    def start_buttons(self):
        """Помещение стартовых кнопок на экран"""
        button_start = self.return_standard_button("Проекты", self.window)
        button_start.bind("<Button-1>", self.make_project_window)
        button_start.pack(anchor=S)

    def standard_window(self, text):
        """Создание базового окна"""
        play_window = Toplevel()
        play_window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())
        play_window.title(text)
        play_window.geometry("1400x900")
        return play_window

    def make_project_window(self, event):
        """Создание окна с проектами"""
        self.window.withdraw()
        project_window = self.standard_window("Проекты")
        project_window.configure(background="blue")
        button_start = self.return_standard_button("Добавить",
                                                   project_window)
        button_start.bind("<Button-1>", lambda e: self.ask_name_project(
            project_window, e))
        button_start.pack(anchor=NE)

    def ask_name_project(self, previous_window, event):
        """Запрос названия проекта"""
        self.name_project = simpledialog.askstring("Введите название проекта",
                                                   "Ввод")
        if self.name_project:
            self.temp_path = self.name_project
            self.make_audio_window(previous_window, self.name_project)
        else:
            print("Ввод был отменен")

    def make_audio_window(self, previous_window, name_project):
        """Создание окна с аудио"""
        previous_window.withdraw()
        audio_window = self.standard_window(name_project)
        (button_split, button_erase, button_speed, button_back, button_next,
         button_save, button_exit) = self.place_all_buttons(
            audio_window)
        arr_buttons = [button_erase, button_speed, button_back, button_next,
                       button_save, button_exit]
        self.place_time_audio(window=audio_window)
        self.check_activity_buttons(arr_buttons)
        self.set_button_functions(arr_buttons, button_split, audio_window)

    def set_button_functions(self, arr_buttons, button_split, window):
        """Установка функций управляющим кнопкам"""
        button_split.bind("<Button-1>", lambda e: self.function_button_split(
            e, window, arr_buttons))
        arr_buttons[0].bind("<Button-1>", lambda e: self.
                            function_button_erase(e, window))
        arr_buttons[1].bind("<Button-1>", lambda e: self.
                            function_button_speed(e, window))
        arr_buttons[4].bind("<Button-1>", self.function_button_save)

    def check_activity_buttons(self, arr_buttons):
        """Проверка на активность кнопок"""
        if self.time == 0:
            for button in arr_buttons:
                button.configure(state=DISABLED)
        else:
            for button in arr_buttons:
                button.configure(state=NORMAL)

    def place_all_buttons(self, audio_window):
        """Создание управляющих кнопок"""
        button_split = self.return_standard_button("Вставить", audio_window)
        button_erase = self.return_standard_button("Обрезать", audio_window)
        button_speed = self.return_standard_button("Скорость", audio_window)
        button_back = self.return_standard_button("Назад", audio_window)
        button_next = self.return_standard_button("Вперед", audio_window)
        button_save = self.return_standard_button("Сохранить", audio_window)
        button_exit = self.return_standard_button("Выйти", audio_window)
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
    def open_file_dialog(type_file='all_types'):
        """Открытие файла определенного типа"""
        if type_file == 'all_types':
            filetypes = [("Audio Files", "*.mp3 *.wav"),
                         ("MP3 Files", "*.mp3"),
                         ("WAV Files", "*.wav")]
        elif type_file == 'mp3':
            filetypes = [("MP3 Files", "*.mp3")]
        else:
            filetypes = [("WAV Files", "*.wav")]

        filename = filedialog.askopenfilename(title="Select a file",
                                              filetypes=filetypes)
        return filename

    @staticmethod
    def draw_plot(window, times, signal_array):
        """Рисование графика"""
        figure = Figure(figsize=(10, 3))
        graphic = figure.add_subplot(111)
        graphic.plot(times, signal_array)
        canvas = FigureCanvasTkAgg(figure, window)
        canvas.draw()
        canvas.get_tk_widget().place(x=10, y=150)

    def plot_mp3_file(self, window, path):
        """Вычисление данных для рисования графика MP3"""
        audio = AudioSegment.from_mp3(path)
        data = np.array(audio.get_array_of_samples())
        if audio.channels == 2:
            data = data[::2]
        times = np.arange(len(data)) / float(audio.frame_rate)
        self.draw_plot(window, times, data)
        self.time = int(audio.duration_seconds)

    def plot_wav_file(self, window):
        """Вычисление данных для рисования графика WAV"""
        audio_data = self.audio.audio_data
        vector_bytes_str = str(audio_data)
        vector_bytes_str_enc = vector_bytes_str.encode()
        bytes_np_dec = vector_bytes_str_enc.decode('unicode-escape').encode(
            'ISO-8859-1')[2:-1]
        num_samples = len(bytes_np_dec) // 2
        bytes_np_dec_aligned = bytes_np_dec[:num_samples * 2]
        signal_array = np.frombuffer(bytes_np_dec_aligned, dtype=np.int16)
        if self.audio.stHeaderFields.num_channels == 2:
            signal_array = signal_array[0::2]
        times = np.arange(len(signal_array)) / float(
            self.audio.stHeaderFields.sample_rate)
        self.draw_plot(window, times, signal_array)
        self.time = int(self.audio.stHeaderFields.size_sec)

    def place_time_audio(self, window):
        """Размещение отметки времени"""
        time_text = str(self.time) + " seconds"
        label = Label(window, text=time_text, font=("Arial", 30))
        label.place(x=100, y=650)
        return label

    def first_split(self, window):
        """Вставка первого куска аудио"""
        path = self.open_file_dialog()
        self.path = path
        if self.path.endswith('.mp3'):
            self.format = 'mp3'
            self.audio = AudiofileMP3(self.path)
            self.plot_mp3_file(window, self.path)
        else:
            self.format = 'wav'
            self.audio = AudiofileWav(self.path)
            self.plot_wav_file(window)

    def function_button_split(self, event, window, arr_buttons):
        """Функция вставки"""
        if self.time == 0:
            self.first_split(window)
        else:
            path = self.open_file_dialog(self.format)
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
        self.place_time_audio(window)
        self.check_activity_buttons(arr_buttons)

    def function_button_erase(self, event, window):
        """Функция обрезки"""
        dialog = TrimDialog(window, "Обрезка", 'erase')
        start = dialog.start
        end = dialog.end
        self.audio.crop_audio(self.temp_path, start, end)
        if self.format == 'mp3':
            self.plot_mp3_file(window, self.temp_path + '.mp3')
        else:
            self.plot_wav_file(window)
        self.place_time_audio(window)

    def function_button_speed(self, event, window):
        """Функция изменения скорости"""
        dialog = TrimDialog(window, "Изменение скорости", 'speed')
        speed = dialog.start
        if self.format == 'mp3':
            self.audio.speed_up_audio(self.temp_path + '.mp3', speed)
            self.plot_mp3_file(window, self.temp_path + '.mp3')
        else:
            self.audio.speed_up_audio(self.temp_path, speed)
            self.plot_wav_file(window)
        self.place_time_audio(window)

    def function_button_save(self, event):
        """Функция сохранения"""
        file_help = FileManager()
        self.path = file_help.save_file_as('.' + self.format)
        self.audio.output_files(self.path)


a = GUI()
a.start_window()
