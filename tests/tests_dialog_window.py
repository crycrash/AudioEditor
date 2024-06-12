import unittest
import tkinter as tk
from front.dialog_window import TrimDialog


class TestTrimDialog(unittest.TestCase):

    def test_body_erase(self):
        root = tk.Tk()
        dialog = TrimDialog(root, type_dialog="erase")
        body_frame = tk.Frame()
        dialog.body(body_frame)
        self.assertIsInstance(dialog.start_entry, tk.Entry)
        self.assertIsInstance(dialog.end_entry, tk.Entry)

    def test_body_split(self):
        root = tk.Tk()
        dialog = TrimDialog(root, type_dialog="split")
        body_frame = tk.Frame()
        dialog.body(body_frame)
        self.assertIsInstance(dialog.start_entry, tk.Entry)
        self.assertIsNone(dialog.end_entry)

    def test_body_speed(self):
        root = tk.Tk()
        dialog = TrimDialog(root, type_dialog="speed")
        body_frame = tk.Frame()
        dialog.body(body_frame)
        self.assertIsInstance(dialog.start_entry, tk.Entry)
        self.assertIsNone(dialog.end_entry)

    def test_body_name(self):
        root = tk.Tk()
        dialog = TrimDialog(root, type_dialog="name")
        body_frame = tk.Frame()
        dialog.body(body_frame)
        self.assertIsInstance(dialog.start_entry, tk.Entry)
        self.assertIsNone(dialog.end_entry)

    def test_apply_erase(self):
        root = tk.Tk()
        dialog = TrimDialog(root, type_dialog="erase")
        dialog.start_entry = tk.Entry()
        dialog.end_entry = tk.Entry()
        dialog.start_entry.insert(0, "10")
        dialog.end_entry.insert(0, "20")
        dialog.apply()
        self.assertEqual(dialog.start, 10)
        self.assertEqual(dialog.end, 20)

    def test_apply_speed(self):
        root = tk.Tk()
        dialog = TrimDialog(root, type_dialog="speed")
        dialog.start_entry = tk.Entry()
        dialog.start_entry.insert(0, "1.5")
        dialog.apply()
        self.assertEqual(dialog.start, 1.5)

    def test_apply_name(self):
        root = tk.Tk()
        dialog = TrimDialog(root, type_dialog="name")
        dialog.start_entry = tk.Entry()
        dialog.start_entry.insert(0, "TestName")
        dialog.apply()
        self.assertEqual(dialog.start, "TestName")

    def test_apply_default(self):
        root = tk.Tk()
        dialog = TrimDialog(root)
        dialog.start_entry = tk.Entry()
        dialog.start_entry.insert(0, "30")
        dialog.apply()
        self.assertEqual(dialog.start, 30)


if __name__ == '__main__':
    unittest.main()
