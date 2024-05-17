from tkinter import filedialog


class FileManager:
    """Класс для работы с файлами через диалоговые окна"""
    @staticmethod
    def open_file():
        """Открытие файла"""
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            print(f"Selected file: {file_path}")
        else:
            print("No file selected")

    @staticmethod
    def save_file_as(extension):
        """Сохранение файла"""
        file_path = filedialog.asksaveasfilename(title="Save As",
                                                 defaultextension=extension)
        if file_path:
            print(f"Selected save path: {file_path}")
        else:
            print("No save path selected")
        print(file_path)
        return file_path
