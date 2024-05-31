from tkinter import *
from tkinter import simpledialog

from back.help_functions import get_folders_with_creation_dates
from back.paths import path_user_data
from front.window_audio_play import WindowAudio


class WindowProjects:
    def __init__(self, window, version_handler, window_helper):
        """Инициация стартового окна"""
        self.window = window
        self.temp_path = ''
        self.version_handler = version_handler
        self.window_helper = window_helper
        self.name_project = ''

    def ask_name_project(self, previous_window, event):
        """Запрос названия проекта"""
        self.name_project = simpledialog.askstring("Введите название проекта",
                                                   "Ввод")
        if self.name_project:
            self.version_handler.make_directory_project(self.name_project)
            self.temp_path = self.version_handler.path + 'temp'
            window_audio = WindowAudio(previous_window,
                                       self.version_handler, self.temp_path,
                                       self.name_project, )
            window_audio.make_audio_window()
        else:
            print("Ввод был отменен")

    def make_project_window(self, event):
        """Создание окна с проектами"""
        self.window.withdraw()
        project_window = self.window_helper.standard_window("Проекты", "1400x900")
        project_window.configure(background="blue")
        button_start = (self.window_helper.
                        return_standard_button("Добавить",
                                               project_window, 15, 5))
        button_start.bind("<Button-1>", lambda e: self.ask_name_project(
            project_window, e))
        self.create_interface(path_user_data, project_window)
        button_start.grid(row=0, column=3)

    def create_interface(self, parent_folder, window):
        """Создает интерфейс с кнопками для папок и метками с датами
        создания"""
        frame = Frame(window)
        frame.grid(row=0, column=0)
        folders = get_folders_with_creation_dates(parent_folder)
        for i, (name, creation_date) in enumerate(folders):
            btn = Button(frame, text=name)
            btn.grid(row=i, column=0, padx=5, pady=5, ipadx=20,
                     ipady=10, sticky=W)
            lbl = Label(frame, text=creation_date)
            lbl.grid(row=i, column=1, padx=5, pady=5, sticky=W)
            btn.bind("<Button-1>",
                     lambda e, folder_name=name: self.open_project(
                         folder_name, window, e))

    def open_project(self, folder_name, previous_window, event):
        """Открытие созданного проекта"""
        self.temp_path = path_user_data + folder_name + '/temp'
        window_audio = WindowAudio(previous_window,
                                   self.version_handler, self.temp_path,
                                   folder_name)
        self.version_handler.path = path_user_data + folder_name + '/'
        window_audio.open_exist_project()
