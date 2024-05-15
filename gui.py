from tkinter import simpledialog, filedialog
from tkinter import *

import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageTk
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure
from pydub import AudioSegment


class GUI:
    def __init__(self):
        """Инициация стартового окна"""
        self.window = Tk()

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
        self.window.withdraw()
        project_window = self.standard_window("Проекты")
        project_window.configure(background="blue")
        button_start = self.return_standard_button("Добавить",
                                                   project_window)
        button_start.bind("<Button-1>", lambda e: self.ask_name_project(
            project_window, e))
        button_start.pack(anchor=NE)

    def ask_name_project(self, previous_window, event):
        name_project = simpledialog.askstring("Введите название проекта",
                                              "Ввод")
        if name_project:
            print(f"Название проекта: {name_project}")
            self.make_audio_window(previous_window, name_project)
        else:
            print("Ввод был отменен")

    def make_audio_window(self, previous_window, name_project):
        previous_window.withdraw()
        audio_window = self.standard_window(name_project)
        (button_split, button_erase, button_speed, button_back, button_next,
         button_save, button_exit) = self.place_all_buttons(
            audio_window)
        button_split.bind("<Button-1>", self.function_button_split)

    def place_all_buttons(self, audio_window):
        button_split = self.return_standard_button("Вставить", audio_window)
        button_erase = self.return_standard_button("Обрезать", audio_window)
        button_speed = self.return_standard_button("Скорость", audio_window)
        button_back = self.return_standard_button("Назад", audio_window)
        button_next = self.return_standard_button("Вперед", audio_window)
        button_save = self.return_standard_button("Сохранить", audio_window)
        button_exit = self.return_standard_button("Выйти", audio_window)
        button_split.grid(row=0, column=0, padx=5, pady=5, sticky="n")
        button_erase.grid(row=0, column=1, padx=5, pady=5, sticky="n")
        button_speed.grid(row=0, column=2, padx=5, pady=5, sticky="n")
        button_next.grid(row=0, column=3, padx=5, pady=5, sticky="n")
        button_back.grid(row=0, column=4, padx=5, pady=5, sticky="n")
        button_save.grid(row=0, column=5, padx=5, pady=5, sticky="n")
        button_exit.grid(row=0, column=6, padx=5, pady=5, sticky="n")
        return (button_split, button_erase, button_speed, button_back,
                button_next, button_save, button_exit)

    def open_file_dialog(self):
        filetypes = [("Audio Files", "*.mp3 *.wav"), ("MP3 Files", "*.mp3"),
                     ("WAV Files", "*.wav")]
        filename = filedialog.askopenfilename(title="Select a file",
                                              filetypes=filetypes)
        if filename:
            print(f"Selected file: {filename}")
            # Здесь можно добавить обработку выбранного файла
        else:
            print("No file selected")
        return filename

    def plot_mp3_file(self, file_path):
        # Чтение MP3 файла
        audio = AudioSegment.from_mp3(file_path)

        # Конвертация аудиоданных в массив numpy
        data = np.array(audio.get_array_of_samples())

        # В случае стерео файла, выбираем только один канал
        if audio.channels == 2:
            data = data[::2]

        # Создание временной оси
        times = np.arange(len(data)) / float(audio.frame_rate)

        # Построение графика
        plt.figure(figsize=(15, 5))
        plt.plot(times, data)
        plt.title('Waveform of {}'.format(file_path))
        plt.ylabel('Amplitude')
        plt.xlabel('Time (s)')
        plt.xlim(0, times[-1])
        plt.show()


    def function_button_split(self, event):
        filename = self.open_file_dialog()
        if filename.endswith('.mp3'):
            self.plot_mp3_file(filename)



a = GUI()
a.start_window()
