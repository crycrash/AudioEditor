import unittest
from unittest.mock import Mock
from tkinter import Button, Toplevel
from front.basic_functions_gui import BasicFunctions


class TestBasicFunctions(unittest.TestCase):

    def test_return_standard_button(self):
        window = Mock()
        button = BasicFunctions.return_standard_button("Test", window, 100, 50)
        self.assertIsInstance(button, Button)
        self.assertEqual(button.cget("text"), "Test")
        self.assertEqual(button.cget("width"), 100)
        self.assertEqual(button.cget("height"), 50)
        self.assertEqual(button.cget("bg"), "white")
        self.assertEqual(button.cget("fg"), "black")

    def test_standard_window(self):
        window = BasicFunctions.standard_window("Test Window", "300x200")
        self.assertIsInstance(window, Toplevel)
        self.assertEqual(window.title(), "Test Window")
        self.assertEqual(window.geometry(), "300x200")


if __name__ == '__main__':
    unittest.main()
