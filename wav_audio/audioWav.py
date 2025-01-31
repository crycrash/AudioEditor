import struct
from wav_audio.dataclass_wav import WavAudioFile as wavAudio


class AudiofileWav:
    """Аудио файл формата WAV"""

    def __init__(self, path):
        """Инициация начальных данных"""
        self.header = b''
        self.audio_data = b''
        self.stHeaderFields = None
        self.path = path
        self.read_data_from_file()

    def read_data_from_file(self):
        """Чтение информации о заголовке и данных из файла"""
        header_size = 44
        with open(self.path, 'rb') as wav_in:
            self.header = wav_in.read(header_size)
            self.audio_data = wav_in.read()
            self.check_wav()
        self.take_header_config()

    def check_wav(self):
        """Проверка файла на принадлежность WAV"""
        riff_string = b'RIFF'
        fmt_string = b'fmt '
        if (self.header[0:4] != riff_string) or \
                (self.header[12:16] != fmt_string):
            raise TypeError("Not valid")

    def output_files(self, path):
        """Вывод данных ы файл"""
        with open(path, 'wb') as wav_out:
            wav_out.write(self.header)
            wav_out.write(self.audio_data)

    def take_header_config(self):
        """Парсинг заголовка wav и высчитывание длины аудио в секундах"""
        chunk_size = struct.unpack('<L',
                                   self.header[4:8])[0]
        num_channels = struct.unpack('<H',
                                     self.header[22:24]
                                     )[0]
        sample_rate = struct.unpack('<L',
                                    self.header[24:28]
                                    )[0]
        bits_per_sample = struct.unpack('<H',
                                        self.header[34:36]
                                        )[0]
        sub_chunk_2_size = struct.unpack('<L',
                                         self.header[40:44]
                                         )[0]

        self.stHeaderFields = wavAudio(chunk_size=chunk_size,
                                       num_channels=num_channels,
                                       sample_rate=sample_rate,
                                       bits_per_sample=bits_per_sample,
                                       sub_chunk_2_size=sub_chunk_2_size,
                                       size_sec=0)
        size_sec = self.count_size_file()
        self.stHeaderFields.size_sec = size_sec

    def count_size_file(self):
        """Подсчет длины аудио фрагмента"""
        count_bytes = self.stHeaderFields.bits_per_sample / 8
        size_file = (self.stHeaderFields.sub_chunk_2_size / count_bytes /
                     self.stHeaderFields.sample_rate
                     / self.stHeaderFields.num_channels)
        return size_file

    def crop_audio(self, path, start_point, end_point):
        """Обрезка файла по указанным секундам"""
        if (start_point > self.stHeaderFields.size_sec or end_point >
                self.stHeaderFields.size_sec):
            raise ValueError('You have gone beyond the allowed length')
        size_header = 36
        count = len(self.audio_data) // self.stHeaderFields.size_sec
        self.audio_data = self.audio_data[int(start_point * count):
                                          int(end_point * count)]
        self.stHeaderFields.sub_chunk_2_size = (self.stHeaderFields.
                                                sub_chunk_2_size // 2)
        self.stHeaderFields.chunk_size = (self.stHeaderFields.
                                          sub_chunk_2_size + size_header)
        self.header = self.header.replace(self.header[40:44],
                                          struct.pack('<L',
                                                      self.
                                                      stHeaderFields.
                                                      sub_chunk_2_size))
        self.header = self.header.replace(self.header[4:8],
                                          struct.pack('<L',
                                                      self.
                                                      stHeaderFields.
                                                      chunk_size))
        self.stHeaderFields.size_sec = end_point - start_point
        self.output_files(path)
        self.path = path

    def splice_audio(self, path, other, time):
        """Вставка одного файла в другой"""
        if time > int(self.stHeaderFields.size_sec):
            raise ValueError('You have gone beyond the allowed length')
        if isinstance(other, AudiofileWav):
            size_header = 36
            count = len(self.audio_data) // self.stHeaderFields.size_sec
            self.audio_data = (self.audio_data[:int(count * time)] +
                               other.audio_data
                               + self.audio_data[int(count * time):])
            self.stHeaderFields.sub_chunk_2_size = (
                    self.stHeaderFields.sub_chunk_2_size
                    + other.stHeaderFields.sub_chunk_2_size)
            self.stHeaderFields.chunk_size = (self.stHeaderFields.
                                              sub_chunk_2_size + size_header)
            self.header = self.header.replace(self.header[40:44],
                                              struct.pack('<L',
                                                          self.
                                                          stHeaderFields.
                                                          sub_chunk_2_size))
            self.header = self.header.replace(self.header[4:8],
                                              struct.pack('<L',
                                                          self.
                                                          stHeaderFields.
                                                          chunk_size))
            self.stHeaderFields.size_sec = (self.stHeaderFields.size_sec +
                                            other.stHeaderFields.size_sec)
            self.output_files(path)

    def speed_up_audio(self, path, speed):
        """Ускорение или замедление аудио дорожки"""
        size_header = 36
        self.stHeaderFields.sample_rate = int(
            self.stHeaderFields.sample_rate * speed)
        self.stHeaderFields.sub_chunk_2_size = int(
            self.stHeaderFields.sub_chunk_2_size * 1 / speed)
        self.stHeaderFields.chunk_size = (
                self.stHeaderFields.sub_chunk_2_size + size_header)
        self.header = self.header.replace(self.header[40:44],
                                          struct.pack('<L',
                                                      self.stHeaderFields.
                                                      sub_chunk_2_size))
        self.header = self.header.replace(self.header[4:8],
                                          struct.pack('<L',
                                                      int(self.stHeaderFields.
                                                          size_sec)))
        self.header = self.header.replace(self.header[24:28], struct.
                                          pack('<L',
                                               self.stHeaderFields.
                                               sample_rate))
        self.stHeaderFields.size_sec = (self.stHeaderFields.size_sec * 1
                                        / speed)
        self.output_files(path)
