import unittest
from unittest.mock import patch, MagicMock

import numpy as np
from matplotlib.figure import Figure
from pydub import AudioSegment
from back.help_functions import (open_file_dialog, draw_plot_back,
                                 plot_mp3_file_back, plot_wav_file_back,
                                 get_folders_with_creation_dates,
                                 parse_file_templates, find_template_info,
                                 count_coordinates)


class TestAudioEditor(unittest.TestCase):

    def test_open_file_dialog(self):
        with patch("tkinter.filedialog.askopenfilename",
                   return_value="dummy_path.mp3"):
            result = open_file_dialog(type_file="mp3")
            self.assertEqual(result, "dummy_path.mp3")

    def test_draw_plot_back(self):
        times = np.linspace(0, 10, 100)
        signal_array = np.sin(times)
        figure = draw_plot_back(times, signal_array)
        self.assertIsInstance(figure, Figure)

    @patch("pydub.AudioSegment.from_mp3")
    @patch("numpy.arange")
    def test_plot_mp3_file_back(self, mock_arange, mock_from_mp3):
        mock_arange.return_value = np.linspace(0, 10, 100)
        mock_from_mp3.return_value = MagicMock(spec=AudioSegment)
        times, data, duration = plot_mp3_file_back("dummy_path.mp3")
        self.assertIsInstance(times, np.ndarray)
        self.assertIsInstance(data, np.ndarray)
        self.assertIsInstance(duration, float)

    def test_plot_wav_file_back(self):
        audio = MagicMock()
        audio.audio_data = b"\x00\x00\x00\x00\x00\x00\x00\x00"
        audio.stHeaderFields.num_channels = 1
        audio.stHeaderFields.sample_rate = 44100
        times, signal_array = plot_wav_file_back(audio)
        self.assertIsInstance(times, np.ndarray)
        self.assertIsInstance(signal_array, np.ndarray)

    @patch("os.listdir", return_value=["folder1", "folder2"])
    @patch("os.path.isdir", return_value=True)
    @patch("os.path.getctime", return_value=1623409644.0490465)
    def test_get_folders_with_creation_dates(self):
        folders_with_dates = get_folders_with_creation_dates("dummy_path")
        self.assertEqual(len(folders_with_dates), 2)
        self.assertIsInstance(folders_with_dates[0], tuple)

    def test_parse_file_templates(self):
        with patch("builtins.open",
                   MagicMock(return_value=["template1 "
                                           "0 None None None None\n"])):
            result, names = parse_file_templates("dummy_path")
            self.assertIsInstance(result, list)
            self.assertIsInstance(names, list)

    def test_find_template_info(self):
        templates = [{"template_name": "template1", "start_time": "0"}]
        template_info = find_template_info(templates, "template1")
        self.assertEqual(template_info["start_time"], "0")
        self.assertIsNone(find_template_info(templates, "template2"))

    def test_count_coordinates(self):
        x_coord, y_coord = count_coordinates(10, 100, 200)
        self.assertIsInstance(x_coord, int)
        self.assertIsInstance(y_coord, int)


if __name__ == '__main__':
    unittest.main()
