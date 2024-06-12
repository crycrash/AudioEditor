import unittest
from unittest.mock import patch, mock_open, MagicMock
from back.version_handler import VersionHandler


class TestVersionHandler(unittest.TestCase):

    @patch("pathlib.Path.mkdir")
    @patch("builtins.open", new_callable=mock_open)
    def test_make_directory_project(self, mock_mkdir):
        handler = VersionHandler()
        handler.make_directory_project("project")
        mock_mkdir.assert_called_once_with("path_to_user_data/project",
                                           parents=True, exist_ok=True)

    @patch("your_module.AudiofileWav")
    @patch("your_module.AudiofileWav.output_files")
    def test_output_first_version(self, mock_output_files):
        handler = VersionHandler()
        handler.format = 'wav'
        handler.first_path = "path_to_first_version.wav"
        handler.output_first_version(MagicMock(), 'wav')
        (mock_output_files.assert_called_once_with
         ("path_to_user_data/first.wav"))

    @patch("builtins.open", new_callable=mock_open)
    def test_write_changes(self, mock_opens):
        """Test write_changes method"""
        handler = VersionHandler()
        handler.path = "path_to_project/"
        handler.pointer = 0
        handler.write_changes('split', 'path_to_audio.wav', start=10)
        mock_opens.assert_called_once_with("path_to_project/versions.txt",
                                           "a+")
        (mock_open().write.assert_called_once_with
         ("split path_to_audio.wav 10\n"))

    @patch("your_module.AudiofileWav")
    @patch("your_module.AudiofileWav.splice_audio")
    def test_operation_process(self, mock_splice_audio):
        handler = VersionHandler()
        handler.format = 'wav'
        handler.first_path = "path_to_first_version.wav"
        handler.operation_process('split',
                                  ['split', 'path_to_audio.wav', '10'],
                                  MagicMock(), "path_to_temp")
        mock_splice_audio.assert_called_once_with("path_to_temp", MagicMock(),
                                                  'path_to_audio.wav', 10)

    def test_check_back_activity(self):
        handler = VersionHandler()
        handler.pointer = 0
        self.assertFalse(handler.check_back_activity())

        handler.pointer = 1
        self.assertTrue(handler.check_back_activity())

    @patch("your_module.AudiofileWav")
    @patch("your_module.AudiofileWav.splice_audio")
    def test_back_changes(self):
        """Test back_changes method"""
        handler = VersionHandler()
        handler.path = "path_to_project/"
        handler.first_path = "path_to_first_version.wav"
        handler.pointer = 2
        handler.data = [['split', 'path_to_audio.wav', '10'],
                        ['split', 'path_to_audio2.wav', '20']]
        handler.back_changes()
        self.assertEqual(handler.pointer, 1)

    @patch("your_module.AudiofileWav")
    @patch("your_module.AudiofileWav.splice_audio")
    def test_next_changes(self):
        handler = VersionHandler()
        handler.path = "path_to_project/"
        handler.first_path = "path_to_first_version.wav"
        handler.pointer = 1
        handler.data = [['split', 'path_to_audio.wav', '10'],
                        ['split', 'path_to_audio2.wav', '20']]
        handler.next_changes()
        self.assertEqual(handler.pointer, 2)

    def test_check_next_activity(self):
        handler = VersionHandler()
        handler.pointer = 0
        handler.data = [['split', 'path_to_audio.wav', '10'],
                        ['split', 'path_to_audio2.wav', '20']]
        self.assertTrue(handler.check_next_activity())
        handler.pointer = 2
        self.assertFalse(handler.check_next_activity())


if __name__ == '__main__':
    unittest.main()
