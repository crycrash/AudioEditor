import os
import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk, Toplevel, Button
from front.window_projects import WindowProjects


class TestWindowProjects(unittest.TestCase):

    def setUp(self):
        self.window = Tk()
        self.version_handler = MagicMock()
        self.window_helper = MagicMock()
        self.project_window = WindowProjects(self.window, self.version_handler,
                                             self.window_helper)

    @patch('tkinter.simpledialog.askstring')
    def test_ask_name_project_with_name(self, mock_askstring):
        mock_askstring.return_value = 'TestProject'
        previous_window = MagicMock()
        with patch('front.window_audio_play.WindowAudio'):
            self.project_window.ask_name_project(previous_window, None)
            self.version_handler.make_directory_project.assert_called_once_with('TestProject')

    @patch('tkinter.simpledialog.askstring')
    def test_ask_name_project_no_name(self, mock_askstring):
        mock_askstring.return_value = None
        previous_window = MagicMock()
        with patch('builtins.print') as mock_print:
            self.project_window.ask_name_project(previous_window, None)
            self.version_handler.make_directory_project.assert_not_called()
            mock_print.assert_called_once_with("Ввод был отменен")

    @patch('back.help_functions.get_folders_with_creation_dates')
    def test_create_interface(self, mock_get_folders):
        mock_get_folders.return_value = [('Project1', '2023-06-10'),
                                         ('Project2', '2023-06-11')]
        window = Toplevel()
        current_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        relative_path_user_data = 'users_data/'
        path_user_data = os.path.join(current_directory,
                                      relative_path_user_data)
        self.project_window.create_interface(path_user_data, window)
        frame = window.children['!frame']

        self.assertEqual(len(frame.children), 6)
        self.assertIsInstance(frame.children['!button'], Button)

    @patch('tkinter.Toplevel')
    def test_make_project_window(self, mock_toplevel):
        mock_toplevel_instance = mock_toplevel.return_value
        self.window_helper.standard_window.return_value \
            = mock_toplevel_instance
        current_directory = os.path.normpath(os.getcwd() + os.sep + os.pardir)
        relative_path_user_data = 'users_data/'
        path_user_data = os.path.join(current_directory,
                                      relative_path_user_data)
        with (patch.object(self.project_window, 'create_interface')
              as mock_create_interface):
            self.project_window.make_project_window(None)
            self.window_helper.standard_window.assert_called_once_with("Проекты", "1400x900")
            self.window_helper.return_standard_button.assert_called_once_with("Добавить", mock_toplevel_instance, 15, 5)
            mock_create_interface.assert_called_once_with(path_user_data, mock_toplevel_instance)


if __name__ == '__main__':
    unittest.main()
