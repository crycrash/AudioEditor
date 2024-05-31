import tkinter as tk
from tkinter import simpledialog


class TrimDialog(simpledialog.Dialog):
    """Класс диалоговых окон для выбора конфигурации функций"""

    def __init__(self, parent, title=None, type_dialog=None):
        """Инициация диалогового окна"""
        self.type = type_dialog
        self.start = None
        self.end = None
        self.start_entry = None
        self.end_entry = None
        super().__init__(parent, title)

    def body(self, master):
        """Создание диалогового окна"""
        if self.type == "erase":
            tk.Label(master, text="Start:").grid(row=0)
            tk.Label(master, text="End:").grid(row=1)
            self.start_entry = tk.Entry(master)
            self.end_entry = tk.Entry(master)
            self.start_entry.grid(row=0, column=1)
            self.end_entry.grid(row=1, column=1)
        elif self.type == "split":
            tk.Label(master, text="Start:").grid(row=0)
            self.start_entry = tk.Entry(master)
            self.start_entry.grid(row=0, column=1)
        elif self.type == 'speed':
            tk.Label(master, text="Speed:").grid(row=0)
            self.start_entry = tk.Entry(master)
            self.start_entry.grid(row=0, column=1)
        elif self.type == 'name':
            tk.Label(master, text="Name:").grid(row=0)
            self.start_entry = tk.Entry(master)
            self.start_entry.grid(row=0, column=1)

        return self.start_entry

    def apply(self):
        """Реакция на подтверждение формы"""
        try:
            if self.type == "erase":
                self.start = int(self.start_entry.get())
                self.end = int(self.end_entry.get())

            elif self.type == 'speed':
                self.start = float(self.start_entry.get())
            elif self.type == 'name':
                self.start = str(self.start_entry.get())
            else:
                self.start = int(self.start_entry.get())

        except ValueError:
            pass
