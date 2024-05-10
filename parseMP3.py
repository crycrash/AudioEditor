import struct
from config import bitrate_table, sample_rate_table
from dataclass_mp3 import Mp3Audio as mp3_audio
from dataclass_MP3_frame import Mp3AudioFrame as mp3_audio_frame


class AudioFrameMp3:
    """Класс с информацией о MP3 фрагменте"""

    def __init__(self, path):
        """Инициализация фрагмента"""
        self.data_example = None
        self.init_data_example(path)

    def init_data_example(self, path):
        """Инициализация датакласса фрагмента"""
        self.data_example = mp3_audio(all_sizes=[], all_headers=[])
        self.data_example.path = path
        with open(self.data_example.path, 'rb') as wav_in:
            self.data_example.raw_data = wav_in.read()
        self.data_example.all_headers = []
        self.data_example.all_sizes = []
        self.data_example.audio_data = b''

    def init_frame_header(self, frame):
        """Инициализация датакласса заголовка"""
        frame_header = struct.unpack("BBBB",
                                     frame.header)
        frame.marker = frame_header[0]
        if frame.marker != 255:
            return -1
        frame.padded = bool(frame_header[2] & 0b10)
        bit_rate_bits = frame_header[2] & 0xf0

        if (frame_header[1] & 0b00001110) != 0b1010:
            raise RuntimeError("Can currently only handle mpeg 1!")

        sample_bytes = (0b00001100 & frame_header[2]) >> 2
        frame.sample_rate = sample_rate_table[sample_bytes]
        self.data_example.sample_rate = frame.sample_rate
        frame.bit_rate_bits = bitrate_table[bit_rate_bits]
        self.data_example.bit_rate = frame.bit_rate_bits
        frame.size = int(
            144 * (1000 * frame.bit_rate_bits) / frame.sample_rate)
        if frame.padded:
            frame.size += 1
        return frame

    def count_size_header(self):
        """Обработка всех заголовков аудио"""
        frame_sizes = []
        frame_idx = 0
        len_header = 4
        len_raw_data = len(self.data_example.raw_data) - len_header
        while frame_idx < len_raw_data:
            frame = mp3_audio_frame
            frame.header = self.data_example.raw_data[frame_idx:
                                                      frame_idx + len_header]
            frame = self.init_frame_header(frame)
            self.data_example.all_headers.append(frame.header)
            frame_sizes.append(frame.size)
            self.data_example.audio_data += self.data_example.raw_data[
                                            frame_idx:frame.size + frame_idx]
            frame_idx = sum(frame_sizes)

        self.data_example.count = len(frame_sizes)
        self.data_example.all_sizes = frame_sizes
        return frame_idx

    def get_tag_length(self):
        """Подсчет длины тэгов"""
        unpacked = struct.unpack("BBBxxBBBBB", self.data_example.raw_data[:10])
        if not all(
                i == j for i, j in zip(unpacked[:3], (ord(i) for i in "ID3"))):
            return 0
        header_size_bytes = unpacked[4:10]
        size_tag = [get_pad(x)[1:] for x in header_size_bytes]
        size_tag = "".join(size_tag)
        size_tag = int(size_tag, 2)
        len_data_tag = 10
        self.data_example.tag = self.data_example.raw_data[:
                                                           size_tag +
                                                           len_data_tag]
        return size_tag + len_data_tag

    def return_audio_data(self):
        """Возвращение аудио данных"""
        self.data_example.raw_data = self.data_example.raw_data[
                                     self.get_tag_length():]
        self.count_size_header()
        self.data_example.size = (len(self.data_example.raw_data) / (
                self.data_example.bit_rate *
                1000)) * 8
        return self.data_example


def get_pad(bn):
    """Перевод в нужный формат"""
    return "{:0>8b}".format(bn)
