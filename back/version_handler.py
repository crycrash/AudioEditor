import os
from pathlib import Path
from wav_audio.audioWav import AudiofileWav
from mp3_audio.audioMP3 import AudiofileMP3


class VersionHandler:
    """Класс-хранитель версий аудио"""
    def __init__(self):
        """Инициализация"""
        self.path = ''
        self.file_versions = ''
        self.pointer = 0
        self.format = None
        self.audio = None
        self.first_path = None
        self.data = None
        self.path_user_data = None
        self.make_user_path()

    def make_user_path(self):
        current_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        relative_path_user_data = 'users_data/'
        self.path_user_data = os.path.join(current_directory,
                                           relative_path_user_data)

    def make_directory_project(self, project_name):
        """Создание папки проекта"""
        self.path = self.path_user_data + project_name
        Path(self.path).mkdir(parents=True, exist_ok=True)
        self.path += '/'
        self.make_list_versions()

    def make_list_versions(self):
        """Создание списка версий"""
        self.file_versions = open(self.path + 'versions.txt', "w+")
        self.file_versions.close()

    def output_first_version(self, audio, format_audio):
        """Запись первой версии"""
        self.first_path = self.path + 'first.' + format_audio
        audio.output_files(self.path + 'first.' + format_audio)
        self.format = format_audio
        if self.format == 'wav':
            self.audio = AudiofileWav(self.first_path)
        else:
            self.audio = AudiofileMP3(self.first_path)

    def write_changes(self, operation, path_split=None, speed=None,
                      start=None, end=None):
        """Запись изменений"""
        self.file_versions = open(self.path + 'versions.txt', "a+")
        if operation == 'split':
            self.file_versions.write('split ' + path_split + ' ' + str(start)
                                     + '\n')
        elif operation == 'erase':
            self.file_versions.write('erase ' + str(start) + ' ' + str(end)
                                     + '\n')
        elif operation == 'speed':
            self.file_versions.write('speed ' + str(speed) + '\n')
        self.pointer += 1
        self.file_versions.close()

    def parse_file_versions(self):
        """Парсинг файла с изменениями"""
        with open(self.path + 'versions.txt', 'r') as file:
            lines = file.readlines()
        self.data = []
        for line in lines:
            line = line.strip()
            fields = line.split()
            self.data.append(fields)

    def back_changes(self):
        """Откат версии"""
        self.parse_file_versions()
        self.pointer -= 1
        if self.format == 'wav':
            audio_temp = AudiofileWav(self.first_path)
        else:
            audio_temp = AudiofileMP3(self.first_path)
        temp_path = self.path + 'temp'
        for i in range(0, self.pointer):
            version = self.data[i]
            operation = version[0]
            self.operation_process(operation, version, audio_temp, temp_path)
        return audio_temp

    def operation_process(self, operation, version, audio_temp, temp_path):
        """Обработка операции"""
        if operation == 'split':
            if self.format == 'wav':
                audio_split = AudiofileWav(version[1])
            else:
                audio_split = AudiofileMP3(version[1])
            audio_temp.splice_audio(temp_path, audio_split, int(version[
                                                                    2]))
        elif operation == 'erase':
            audio_temp.crop_audio(temp_path, int(version[1]),
                                  int(version[2]))

        elif operation == 'speed':
            audio_temp.speed_up_audio(temp_path, float(version[1]))

    def check_back_activity(self):
        """Проверка на возможность отката"""
        if self.pointer == 0:
            return False
        else:
            return True

    def next_changes(self):
        """Возврат изменений"""
        self.parse_file_versions()
        self.pointer += 1
        temp_path = self.path + 'temp'
        if self.format == 'wav':
            audio_temp = AudiofileWav(temp_path + '.wav')
        else:
            audio_temp = AudiofileMP3(temp_path + '.mp3')
            temp_path += '.mp3'
        version = self.data[self.pointer - 1]
        operation = version[0]
        self.operation_process(operation, version, audio_temp, temp_path)
        return audio_temp

    def check_next_activity(self):
        """Проверка на возможность возврата изменений"""
        self.parse_file_versions()
        if (self.data is None) or (self.pointer == len(self.data)):
            return False
        else:
            return True
