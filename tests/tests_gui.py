import unittest
from unittest.mock import patch
from tkinter import Tk
from front.gui import GUI
from back.version_handler import VersionHandler
from front.basic_functions_gui import BasicFunctions


class TestGUI(unittest.TestCase):

    @patch('tkinter.Tk', autospec=True)
    @patch('back.version_handler.VersionHandler', autospec=True)
    @patch('front.basic_functions_gui.BasicFunctions', autospec=True)
    def setUp(self, mock_basic_functions, mock_version_handler, mock_tk):
        self.mock_tk = mock_tk.return_value
        self.mock_version_handler = mock_version_handler.return_value
        self.mock_basic_functions = mock_basic_functions.return_value
        self.gui = GUI()

    def test_init(self):
        self.assertIsInstance(self.gui.window, Tk)
        self.assertEqual(self.gui.time, 0)
        self.assertIsNone(self.gui.audio)
        self.assertIsNone(self.gui.path)
        self.assertEqual(self.gui.temp_path, '')
        self.assertEqual(self.gui.name_project, '')
        self.assertEqual(self.gui.format, '')
        self.assertIsNone(self.gui.label)
        self.assertIsInstance(self.gui.version_handler, VersionHandler)
        self.assertIsInstance(self.gui.window_helper, BasicFunctions)


if __name__ == '__main__':
    unittest.main()
