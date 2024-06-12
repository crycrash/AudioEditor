import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from front.equalizer import Equalizer
from pydub import AudioSegment
import plotly.graph_objs as go


class TestEqualizer(unittest.TestCase):

    def setUp(self):
        self.path_audio = 'test.mp3'
        self.format_audio = 'mp3'
        self.window = MagicMock()
        self.equalizer = Equalizer(self.path_audio, self.format_audio,
                                   self.window)

    @patch('pydub.AudioSegment.from_mp3')
    def test_open_audio_mp3(self, mock_from_mp3):
        self.equalizer.open_audio()
        mock_from_mp3.assert_called_once_with(self.path_audio)
        self.assertIsInstance(self.equalizer.audio, MagicMock)

    @patch('pydub.AudioSegment.from_wav')
    def test_open_audio_wav(self, mock_from_wav):
        self.equalizer.format = 'wav'
        self.equalizer.open_audio()
        mock_from_wav.assert_called_once_with(self.path_audio)
        self.assertIsInstance(self.equalizer.audio, MagicMock)

    def test_butter_bandpass(self):
        low_cut = 20
        high_cut = 2000
        sampling_rate = 44100
        order = 10
        first_cf, second_cf = self.equalizer.butter_bandpass(low_cut, high_cut,
                                                             sampling_rate)
        self.assertEqual(len(first_cf), order + 1)
        self.assertEqual(len(second_cf), order + 1)

    def test_bandpass_filter(self):
        data = np.random.randn(1000)
        low_cut = 20
        high_cut = 2000
        sampling_rate = 44100
        order = 5
        filtered_data = self.equalizer.bandpass_filter(data, low_cut, high_cut,
                                                       sampling_rate, order)
        self.assertEqual(len(filtered_data), len(data))

    @patch.object(Equalizer, 'apply_filters')
    def test_save_file(self, mock_apply_filters):
        mock_apply_filters.return_value = AudioSegment.empty()
        self.equalizer.low_slider = MagicMock()
        self.equalizer.mid_slider = MagicMock()
        self.equalizer.high_slider = MagicMock()
        self.equalizer.low_slider.get.return_value = 5
        self.equalizer.mid_slider.get.return_value = 5
        self.equalizer.high_slider.get.return_value = 5
        with patch.object(AudioSegment, 'export') as mock_export:
            self.equalizer.save_file()
            mock_apply_filters.assert_called_once()
            mock_export.assert_called_once()

    @patch.object(Equalizer, 'execute_filtration')
    def test_create_figure(self, mock_execute_filtration):
        samples = np.random.randn(1000)
        mock_execute_filtration.return_value = AudioSegment(
            samples.tobytes(),
            frame_rate=44100,
            sample_width=2,
            channels=1
        )
        self.equalizer.audio = AudioSegment(
            samples.tobytes(),
            frame_rate=44100,
            sample_width=2,
            channels=1
        )

        fig = self.equalizer.create_figure()
        self.assertIsInstance(fig, go.Figure)


if __name__ == '__main__':
    unittest.main()
