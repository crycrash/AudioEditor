from tkinter import *


class BasicFunctions:
    """Базовые функции для работы с графическим интерфейсом"""
    @staticmethod
    def return_standard_button(text, window):
        """Cоздание базовой кнопки"""
        button = Button(window,
                        text=text,
                        width=15, height=5,
                        bg='white', fg="black"
                        )
        return button

    @staticmethod
    def standard_window(text):
        """Создание базового окна"""
        play_window = Toplevel()
        play_window.protocol("WM_DELETE_WINDOW", lambda: play_window.destroy())
        play_window.title(text)
        play_window.geometry("1400x900")
        return play_window
