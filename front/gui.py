from tkinter import *
from back.version_handler import VersionHandler
from front.basic_functions_gui import BasicFunctions
from front.window_projects import WindowProjects


class GUI:
    """Основной класс графического интерфейса"""
    def __init__(self):
        """Инициация стартового окна"""
        self.window = Tk()
        self.time = 0
        self.audio = None
        self.path = None
        self.temp_path = ''
        self.name_project = ''
        self.format = ''
        self.label = None
        self.version_handler = VersionHandler()
        self.window_helper = BasicFunctions()

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

    def start_buttons(self):
        """Помещение стартовых кнопок на экран"""
        button_start = self.window_helper.return_standard_button("Проекты",
                                                                 self.window)
        window_prod = WindowProjects(self.window, self.version_handler,
                                     self.window_helper)
        button_start.bind("<Button-1>", window_prod.make_project_window)
        button_start.pack(anchor=S)


a = GUI()
a.start_window()
