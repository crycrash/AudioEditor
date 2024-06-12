import unittest
from unittest.mock import patch, mock_open
from wav_audio.dataclass_wav import WavAudioFile as wavAudio
from wav_audio.audioWav import AudiofileWav


class TestAudiofileWav(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.audiofile = AudiofileWav("test.wav")

    def test_init(self):
        """Тестирование инициализации"""
        self.assertEqual(self.audiofile.path, "test.wav")
        self.assertTrue(len(self.audiofile.header) > 0)
        self.assertTrue(len(self.audiofile.audio_data) > 0)

    def test_check_wav(self):
        """Тестирование проверки формата WAV"""
        data = str('RIIF' + '\x00' * 8 + 'fmt ' + '\x00' * 100)
        with open('dummy_path.wav', 'w+') as file:
            file.write(data)
        self.audiofile.check_wav()
        with self.assertRaises(Exception):
            AudiofileWav("dummy_path.wav")

    def test_take_header_config(self):
        """Тестирование парсинга заголовка"""
        self.audiofile.take_header_config()
        self.assertEqual(self.audiofile.stHeaderFields.chunk_size, 1691172)
        self.assertEqual(self.audiofile.stHeaderFields.num_channels, 2)
        self.assertEqual(self.audiofile.stHeaderFields.sample_rate, 44100)
        self.assertEqual(self.audiofile.stHeaderFields.bits_per_sample, 16)
        self.assertEqual(self.audiofile.stHeaderFields.sub_chunk_2_size,
                         1691136)
        self.assertEqual(self.audiofile.stHeaderFields.size_sec,
                         self.audiofile.count_size_file())

    def test_count_size_file(self):
        """Тестирование подсчета длины аудиофайла"""
        self.audiofile.stHeaderFields = wavAudio(
            chunk_size=36,
            num_channels=2,
            sample_rate=44100,
            bits_per_sample=16,
            sub_chunk_2_size=1000,
            size_sec=0
        )
        size_sec = self.audiofile.count_size_file()
        expected_size_sec = 1000 / (16 / 8) / 44100 / 2
        self.assertAlmostEqual(size_sec, expected_size_sec)

    @patch("builtins.open", new_callable=mock_open)
    def test_output_files(self, mock_file):
        """Тестирование вывода данных в файл"""
        self.audiofile.header = b'RIFF' + b'\x00' * 36 + b'fmt ' + b'\x00' * 24
        self.audiofile.audio_data = b'\x00' * 100
        self.audiofile.output_files("output_path")
        mock_file.assert_called_with("output_path", "wb")
        handle = mock_file()
        handle.write.assert_any_call(self.audiofile.header)
        handle.write.assert_any_call(self.audiofile.audio_data)

    def test_crop_audio(self):
        """Тестирование обрезки аудио"""
        self.audiofile.stHeaderFields = wavAudio(
            chunk_size=36,
            num_channels=2,
            sample_rate=44100,
            bits_per_sample=16,
            sub_chunk_2_size=1000,
            size_sec=10
        )
        self.audiofile.audio_data = b'\x00' * 1000
        self.audiofile.crop_audio("output_path", 2, 5)
        self.assertEqual(len(self.audiofile.audio_data), 300)
        self.assertEqual(self.audiofile.stHeaderFields.size_sec, 3)

    def test_speed_up_audio(self):
        """Тестирование ускорения аудио"""
        self.audiofile.stHeaderFields = wavAudio(
            chunk_size=36,
            num_channels=2,
            sample_rate=44100,
            bits_per_sample=16,
            sub_chunk_2_size=1000,
            size_sec=10
        )
        self.audiofile.audio_data = b'\x00' * 1000
        self.audiofile.speed_up_audio("output_path", 2)
        self.assertEqual(self.audiofile.stHeaderFields.sample_rate, 88200)
        self.assertEqual(self.audiofile.stHeaderFields.size_sec, 5)
        self.assertEqual(self.audiofile.stHeaderFields.sub_chunk_2_size, 500)


if __name__ == '__main__':
    unittest.main()
