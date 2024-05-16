from pathlib import Path
from wav_audio.audioWav import AudiofileWav
from front.dialog_window import TrimDialog
from mp3_audio.audioMP3 import AudiofileMP3
from front.file_helper import FileManager


class VersionHandler:
    def __init__(self):
        self.path = ''
        self.file_versions = ''
        self.pointer = 0
        self.format = None
        self.audio = None
        self.first_path = None

    def make_directory_project(self, project_name):
        self.path = ('/Users/milana/PycharmProjects/audioEditor/users_data/'
                     + project_name)
        Path(self.path).mkdir(parents=True, exist_ok=True)
        self.path += '/'
        self.make_list_versions()

    def make_list_versions(self):
        self.file_versions = open(self.path + 'versions.txt', "w+")
        self.file_versions.close()

    def output_first_version(self, audio, format_audio):
        self.first_path = self.path + 'first.' + format_audio
        audio.output_files(self.path + 'first.' + format_audio)
        self.format = format_audio
        if self.format == 'wav':
            self.audio = AudiofileWav(self.first_path)
        else:
            self.audio = AudiofileMP3(self.first_path)

    def write_changes(self, operation, path_split=None, speed=None,
                      start=None, end=None):
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
        with open(self.path + 'versions.txt', 'r') as file:
            lines = file.readlines()
        parsed_data = []
        for line in lines:
            line = line.strip()
            fields = line.split()
            parsed_data.append(fields)
        return parsed_data

    def back_changes(self):
        data = self.parse_file_versions()
        self.pointer -= 1
        if self.format == 'wav':
            audio_temp = AudiofileWav(self.first_path)
        else:
            audio_temp = AudiofileMP3(self.first_path)
        temp_path = self.path + 'temp'
        for i in range(0, self.pointer):
            version = data[i]
            operation = version[0]
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
        return audio_temp
