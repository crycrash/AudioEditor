import unittest
from unittest.mock import patch, MagicMock, mock_open
from mp3_audio.audioMP3 import AudiofileMP3


class TestAudiofileMP3(unittest.TestCase):

    def setUp(self):
        self.path = 'test.mp3'
        self.audio_frame_mock = MagicMock()
        self.audio_mock = MagicMock()
        self.audio_mock.raw_data = b'test_audio_data'
        self.audio_mock.size = 100
        self.audio_frame_mock.return_audio_data.return_value = self.audio_mock
        self.audio_frame_mock.data_example.all_headers = [b'header1',
                                                          b'header2']
        self.audio_frame_mock.data_example.all_sizes = [100, 200]

        patcher1 = patch('mp3_audio.parseMP3.AudioFrameMp3',
                         return_value=self.audio_frame_mock)
        self.addCleanup(patcher1.stop)
        self.MockFrameHeader = patcher1.start()

        self.audiofile = AudiofileMP3(self.path)

    def test_init(self):
        self.assertEqual(self.audiofile.path, self.path)
        self.assertEqual(self.audiofile.frames_headers[0],
                         b'\xff\xfbP\x00')
        self.assertEqual(self.audiofile.sizes_headers[1], 417)
        self.assertEqual(self.audiofile.format, '.mp3')

    def test_output_files(self):
        with patch('builtins.open', mock_open()) as mocked_file:
            self.audiofile.output_files('output.mp3')
            mocked_file.assert_called_once_with('output.mp3', 'wb')

    def test_crop_audio_valid(self):
        with patch.object(self.audiofile, 'output_files') as mock_output_files:
            self.audiofile.crop_audio('cropped', 1, 3)
            mock_output_files.assert_called_once_with('cropped.mp3')
            self.assertEqual(self.audiofile.audio.size, 2)
            self.assertEqual(self.audiofile.path, 'cropped')

    def test_crop_audio_invalid(self):
        with self.assertRaises(ValueError):
            self.audiofile.crop_audio('cropped', 1000, 2000)

    def test_splice_audio_valid(self):
        other = MagicMock()
        other.audio_data = b'other_audio_data'
        other.audio.size = 50
        with patch.object(self.audiofile, 'output_files') as mock_output_files:
            self.audiofile.splice_audio('spliced', other, 1)
            mock_output_files.assert_called_once_with('spliced.mp3')
            self.assertEqual(self.audiofile.path, 'spliced')

    def test_splice_audio_invalid(self):
        other = MagicMock()
        other.audio_data = b'other_audio_data'
        other.audio.size = 50
        with self.assertRaises(Exception):
            self.audiofile.splice_audio('spliced', other, 1000)

    def test_speed_up_audio(self):
        self.audiofile.speed_up_audio('speed.mp3', 2.0)
        self.assertEqual(int(self.audiofile.audio.size), 3)
        self.assertEqual(self.audiofile.path, 'speed.mp3')


if __name__ == '__main__':
    unittest.main()
