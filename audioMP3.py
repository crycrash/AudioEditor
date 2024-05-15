from parseMP3 import AudioFrameMp3 as frameHeader
from pydub import AudioSegment
from pydub import effects
from audioWav import AudiofileWav


class AudiofileMP3:

    def __init__(self, path):
        """"Инициализация аудио фрагмента"""
        self.path = path
        self.audio_frame = frameHeader(path)
        self.audio = self.audio_frame.return_audio_data()
        self.audio_data = self.audio.raw_data
        self.frames_headers = self.audio_frame.data_example.all_headers
        self.sizes_headers = self.audio_frame.data_example.all_sizes

    def output_files(self, path):
        """"Вывод в файл"""
        with open(path, 'wb') as wav_out:
            wav_out.write(self.audio_data)

    def crop_audio(self, path, start_point, end_point):
        """Обрезка файла по указанным секундам"""
        if (start_point > self.audio.size or end_point >
                self.audio.size):
            raise Exception('You have gone beyond the allowed length')
        frame_start = int(len(self.audio_data) // self.audio.size)
        frame_end = frame_start * end_point
        frame_start = frame_start * start_point
        new_data = self.audio_data[frame_start:frame_end]
        self.audio_data = new_data
        self.output_files(path)
        self.audio.size = end_point - start_point
        self.path = path

    def splice_audio(self, path, other, start_point):
        """Вставка одного аудио файла в другой"""
        if start_point > int(self.audio.size):
            raise Exception('You have gone beyond the allowed length')
        frame_start = int(len(self.audio_data) // self.audio.size)
        frame_start = frame_start * start_point
        insert_data = other.audio_data
        output_data = (self.audio_data[:frame_start] + insert_data
                       + self.audio_data[frame_start:])
        self.audio_data = output_data
        self.output_files(path)
        self.audio.size += other.audio.size
        self.path = path

    def speed_up_audio(self, path, speed=2.0):
        """Ускорение аудио"""
        sound = AudioSegment.from_mp3(self.path)
        so = sound.speedup(speed, 150, 25)
        so.export(path, format="mp3")
        self.path = path



a = AudiofileMP3('/Users/milana/Downloads/sample4.mp3')
a.crop_audio('/Users/milana/Downloads/skj123.mp3', 5, 17)
a.speed_up_audio('/Users/milana/Downloads/skj123.mp3', 1.5)
b = AudiofileMP3('/Users/milana/Downloads/sample-9s.mp3')
c = AudiofileMP3('/Users/milana/Downloads/skj123.mp3')
b.splice_audio('/Users/milana/Downloads/skjxc4.mp3', c, 2)
