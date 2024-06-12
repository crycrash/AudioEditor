import unittest
from unittest.mock import patch
from front.file_helper import FileManager


class TestFileManager(unittest.TestCase):

    def test_open_file_selected(self, mock_askopenfilename):
        mock_askopenfilename.return_value = '/path/to/selected/file.txt'

        with patch('builtins.print') as mock_print:
            FileManager.open_file()
            mock_print.assert_called_once_with(
                "Selected file: /path/to/selected/file.txt")

    def test_open_file_not_selected(self, mock_askopenfilename):
        mock_askopenfilename.return_value = ''

        with patch('builtins.print') as mock_print:
            FileManager.open_file()
            mock_print.assert_called_once_with("No file selected")

    def test_save_file_as_selected(self, mock_asksaveasfilename):
        mock_asksaveasfilename.return_value = '/path/to/save/file.txt'

        with patch('builtins.print') as mock_print:
            result = FileManager.save_file_as('.txt')
            mock_print.assert_called_with(
                "Selected save path: /path/to/save/file.txt")
            self.assertEqual(result, '/path/to/save/file.txt')

    def test_save_file_as_not_selected(self, mock_asksaveasfilename):
        mock_asksaveasfilename.return_value = ''

        with patch('builtins.print') as mock_print:
            result = FileManager.save_file_as('.txt')
            mock_print.assert_called_with("No save path selected")
            self.assertEqual(result, '')


if __name__ == '__main__':
    unittest.main()
