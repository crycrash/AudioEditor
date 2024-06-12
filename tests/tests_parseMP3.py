import unittest
from unittest.mock import patch, mock_open
from mp3_audio.config import bitrate_table, sample_rate_table
from mp3_audio.dataclass_MP3_frame import Mp3AudioFrame as mp3AudioFrame
from mp3_audio.parseMP3 import AudioFrameMp3, get_pad


class TestAudioFrameMp3(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open,
           read_data=b'\xff\xfa\xb0\x64' * 10)
    def setUp(self, mock_file):
        """Настройка перед каждым тестом"""
        self.audio_frame = AudioFrameMp3("dummy_path")

    def test_init_data_example(self):
        """Тестирование инициализации данных примера"""
        self.assertIsNotNone(self.audio_frame.data_example)
        self.assertEqual(self.audio_frame.data_example.path, "dummy_path")
        self.assertTrue(len(self.audio_frame.data_example.raw_data) > 0)
        self.assertEqual(self.audio_frame.data_example.all_headers, [])
        self.assertEqual(self.audio_frame.data_example.all_sizes, [])
        self.assertEqual(self.audio_frame.data_example.audio_data, b'')

    def test_init_frame_header(self):
        """Тестирование инициализации заголовка фрейма"""
        header = [b'\xff\xfa\xb0\x64']
        frame = mp3AudioFrame(header, 255, True, 64)
        result = self.audio_frame.init_frame_header(frame)
        self.assertNotEqual(result, -1)
        self.assertTrue(frame.padded)
        self.assertEqual(frame.sample_rate,
                         sample_rate_table[(0b00001100 & 0xb0) >> 2])
        self.assertEqual(frame.bit_rate_bits, bitrate_table[0xb0 & 0xf0])
        self.assertGreater(frame.size, 0)

    def test_count_size_header(self):
        """Тестирование подсчета размеров заголовков"""
        self.audio_frame.data_example.raw_data = b'\xff\xfa\xb0\x64' * 10
        frame_idx = self.audio_frame.count_size_header()
        self.assertEqual(self.audio_frame.data_example.count, 10)
        self.assertEqual(frame_idx,
                         sum(self.audio_frame.data_example.all_sizes))
        self.assertTrue(len(self.audio_frame.data_example.audio_data) > 0)

    @patch("struct.unpack", return_value=(0x49, 0x44, 0x33, 0, 0, 0, 0, 0x0a))
    def test_get_tag_length(self, mock_unpack):
        """Тестирование получения длины тэгов"""
        self.audio_frame.data_example.raw_data =\
            b"ID3\x03\x00\x00\x00\x00\x00\x0a" + b'\xff\xfa\xb0\x64' * 10
        tag_length = self.audio_frame.get_tag_length()
        self.assertEqual(tag_length, 20)
        self.assertEqual(len(self.audio_frame.data_example.tag), 20)

    @patch("builtins.open", new_callable=mock_open,
           read_data=b"ID3\x03\x00\x00\x00\x00\x00\x0a" + b'\xff\xfa\xb0\x64'
                     * 10)
    def test_return_audio_data(self):
        """Тестирование возвращения аудио данных"""
        result = self.audio_frame.return_audio_data()
        self.assertIsNotNone(result)
        self.assertTrue(len(result.raw_data) > 0)
        self.assertEqual(result.size,
                         (len(result.raw_data) / (result.bit_rate * 1000)) * 8)

    def test_get_pad(self):
        """Тестирование функции get_pad"""
        result = get_pad(5)
        self.assertEqual(result, "00000101")


if __name__ == '__main__':
    unittest.main()
