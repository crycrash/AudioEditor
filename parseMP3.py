import struct
from config import bitrate_table, sample_rate_table
from dataclass_mp3 import Mp3Audio


class AudioFrameMp3:
    """Класс с информацией о MP3 фрагменте"""
    def __init__(self, path):
        """Инициализация фрагмента"""
        self.data_example = Mp3Audio
        self.init_data_example(path)

    def init_data_example(self, path):
        """Инициализация датакласса фрагмента"""
        self.data_example.path = path
        with open(self.data_example.path, 'rb') as wav_in:
            self.data_example.raw_data = wav_in.read()
        self.data_example.audio_data = b''
        self.data_example.bit_rate = 0
        self.data_example.sample_rate = 0
        self.data_example.size = 0
        self.data_example.tag = b''
        self.data_example.count = 0
        self.data_example.all_headers = []
        self.data_example.all_sizes = []



    def count_size_header(self):
        frame_sizes = []
        frame_idx = 0
        len_header = 4
        len_raw_data = len(self.raw_data) - len_header
        while frame_idx < len_raw_data:
            frame_header = self.raw_data[frame_idx:frame_idx + len_header]
            self.data_example.all_headers.append(frame_header)
            frame_header = struct.unpack("BBBB",
                                         frame_header)

            if frame_header[0] != 255:
                break

            padded = bool(frame_header[2] & 0b10)
            bit_rate_bits = frame_header[2] & 0xf0

            if (frame_header[1] & 0b00001110) != 0b1010:
                raise RuntimeError("Can currently only handle mpeg 1!")

            sample_bytes = (0b00001100 & frame_header[2]) >> 2
            self.sample_rate = sample_rate_table[sample_bytes]
            self.bit_rate = bitrate_table[bit_rate_bits]
            frame_size = int(
                144 * (1000 * self.bit_rate) / self.sample_rate)

            if padded:
                frame_size += 1
            frame_sizes.append(frame_size)
            self.audio_data += self.raw_data[
                             frame_idx:frame_size + frame_idx]
            frame_idx = sum(frame_sizes)

        self.count = len(frame_sizes)
        self.data_example.all_sizes = frame_sizes
        return frame_idx

    def get_tag_length(self):
        unpacked = struct.unpack("BBBxxBBBBB", self.raw_data[:10])
        if not all(
                i == j for i, j in zip(unpacked[:3], (ord(i) for i in "ID3"))):
            return 0
        header_size_bytes = unpacked[4:10]
        size_tag = [get_pad(x)[1:] for x in header_size_bytes]
        size_tag = "".join(size_tag)
        size_tag = int(size_tag, 2)
        self.tag = self.raw_data[:size_tag + 10]
        return size_tag + 10

    def return_audio_data(self):
        self.raw_data = self.raw_data[self.get_tag_length():]
        self.count_size_header()
        self.size = (len(self.raw_data) / (self.bit_rate *
                                           1000))*8
        return self.audio_data


def get_pad(bn):
    return "{:0>8b}".format(bn)
