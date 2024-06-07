import os
from datetime import datetime
from tkinter import filedialog

import numpy as np
from matplotlib.figure import Figure
from pydub import AudioSegment#plotty


def open_file_dialog(type_file='all_types'):
    """Открытие файла определенного типа"""
    if type_file == 'all_types':
        filetypes = [("Audio Files", "*.mp3 *.wav"),
                     ("MP3 Files", "*.mp3"),
                     ("WAV Files", "*.wav")]
    elif type_file == 'mp3':
        filetypes = [("MP3 Files", "*.mp3")]
    else:
        filetypes = [("WAV Files", "*.wav")]

    filename = filedialog.askopenfilename(title="Select a file",
                                          filetypes=filetypes)
    return filename


def draw_plot_back(times, signal_array):
    """Рисование графика"""
    figure = Figure(figsize=(10, 3))
    graphic = figure.add_subplot(111)
    graphic.plot(times, signal_array)
    return figure


def plot_mp3_file_back(path):
    """Вычисление данных для рисования графика MP3"""
    audio = AudioSegment.from_mp3(path)
    data = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        data = data[::2]
    times = np.arange(len(data)) / float(audio.frame_rate)
    return times, data, audio.duration_seconds


def plot_wav_file_back(audio):
    """Вычисление данных для рисования графика WAV"""
    audio_data = audio.audio_data
    vector_bytes_str = str(audio_data)
    vector_bytes_str_enc = vector_bytes_str.encode()
    bytes_np_dec = vector_bytes_str_enc.decode('unicode-escape').encode(
        'ISO-8859-1')[2:-1]
    num_samples = len(bytes_np_dec) // 2
    bytes_np_dec_aligned = bytes_np_dec[:num_samples * 2]
    signal_array = np.frombuffer(bytes_np_dec_aligned, dtype=np.int16)
    if audio.stHeaderFields.num_channels == 2:
        signal_array = signal_array[0::2]
    times = np.arange(len(signal_array)) / float(
        audio.stHeaderFields.sample_rate)
    return times, signal_array


def get_folders_with_creation_dates(parent_folder):
    """Возвращает список кортежей (название папки, дата создания) для всех
    папок в указанной директории."""
    folders_with_dates = []
    for folder_name in os.listdir(parent_folder):
        folder_path = os.path.join(parent_folder, folder_name)
        if os.path.isdir(folder_path):
            creation_time = os.path.getctime(folder_path)
            creation_date = (datetime.fromtimestamp(creation_time).
                             strftime('%Y-%m-%d %H:%M:%S'))
            folders_with_dates.append((folder_name, creation_date))
    return folders_with_dates


def parse_file(filepath):
    result = []
    names = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                continue
            template_name, rest = parts
            rest_parts = rest.split()
            start_time = rest_parts[0] if rest_parts[0] != 'None' else None
            end_time = rest_parts[1] if rest_parts[1] != 'None' else None
            insert_path = rest_parts[2] if rest_parts[2] != 'None' else None
            insert_time = rest_parts[3] if rest_parts[3] != 'None' else None
            speed = rest_parts[4] if len(rest_parts) > 4 and rest_parts[
                4] != 'None' else None
            names.append(template_name)
            result.append({
                'template_name': template_name,
                'start_time': start_time,
                'end_time': end_time,
                'insert_path': insert_path,
                'insert_time': insert_time,
                'speed': speed
            })
    return result, names


def find_template_info(result, template_name):
    for template in result:
        if template['template_name'] == template_name:
            return template
    return None
