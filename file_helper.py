from tkinter import filedialog


class FileManager:

    @staticmethod
    def open_file():
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            print(f"Selected file: {file_path}")
        else:
            print("No file selected")

    @staticmethod
    def save_file_as(extension):
        file_path = filedialog.asksaveasfilename(title="Save As",
                                                 defaultextension=extension)
        if file_path:
            print(f"Selected save path: {file_path}")
        else:
            print("No save path selected")
        return file_path
