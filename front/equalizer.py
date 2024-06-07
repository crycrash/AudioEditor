import tkinter as tk
from pydub import AudioSegment
from scipy.signal import butter, lfilter
import numpy as np
from basic_functions_gui import BasicFunctions
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
import threading
import webview
from flask import Flask
from back.equalizer_constants import consts


class Equalizer:
    """Эквалайзер"""

    def __init__(self, path_audio, format_audio, window):
        self.low_slider = None
        self.mid_slider = None
        self.high_slider = None
        self.audio = None
        self.path = path_audio
        self.format = format_audio
        self.open_audio()
        self.helper = BasicFunctions()
        self.window = window
        self.wav_format = 'wav'

    def open_audio(self):
        """Открытие файла"""
        if self.format == self.wav_format:
            self.audio = AudioSegment.from_wav(self.path)
        else:
            self.audio = AudioSegment.from_mp3(self.path)

    @staticmethod
    def butter_bandpass(low_cut, high_cut, sampling_rate, order=5):
        """Возвращает коэфициенты фильтра"""
        nyquist_frequency = consts['normalization'] * sampling_rate
        low_normalization = low_cut / nyquist_frequency
        high_normalization = high_cut / nyquist_frequency
        if high_normalization >= consts['full_normalization']:
            high_normalization = 0.99
        if low_normalization >= high_normalization:
            low_normalization = high_normalization - 0.01

        first_coefficient, second_coefficient = butter(order,
                                                       [low_normalization,
                                                        high_normalization],
                                                       btype='band')

        return first_coefficient, second_coefficient

    def bandpass_filter(self, data, low_cut, high_cut, sampling_rate, order=5):
        """Фильтрует сигнал"""
        first_cf, second_cf = self.butter_bandpass(low_cut, high_cut,
                                                   sampling_rate, order=order)
        filtered_signal = lfilter(first_cf, second_cf, data)
        return filtered_signal

    def apply_filters(self, filter_ranges):
        """Возвращает отфильтрованное аудио"""
        samples = np.array(self.audio.get_array_of_samples(),
                           dtype=np.float64)
        sample_rate = self.audio.frame_rate
        filtered_samples = np.zeros_like(samples)
        for low_cut, high_cut, gain in filter_ranges:
            filtered = self.bandpass_filter(samples, low_cut, high_cut,
                                            sample_rate)
            filtered_samples += gain * filtered
        filtered_samples = np.clip(filtered_samples, consts['low_limit'],
                                   consts['upper_limit'])
        filtered_samples = np.nan_to_num(filtered_samples)
        filtered_samples = filtered_samples.astype(np.int16)
        return AudioSegment(
            filtered_samples.tobytes(),
            frame_rate=self.audio.frame_rate,
            sample_width=self.audio.sample_width,
            channels=self.audio.channels
        )

    def save_file(self):
        """Сохранение отфильтрованного аудио"""

        if self.audio:
            output_audio = self.apply_filters([
                (consts['low_rate_start'], consts['middle_rate_start'],
                 self.low_slider.get() / consts["coefficient_normalization"]),
                (consts['middle_rate_start'], consts['high_rate_start'],
                 self.mid_slider.get() / consts["coefficient_normalization"]),
                (consts['high_rate_start'], consts['high_rate_end'],
                 self.high_slider.get() / consts["coefficient_normalization"])
            ])
            output_audio.export(self.path, format="mp3")

    def update_plot(self):
        """Обновление графика"""
        server = Flask(__name__)
        app = dash.Dash(__name__, server=server)
        fig = self.create_figure()
        app.layout = html.Div(children=[
            html.H1(children='Частоты аудио'),
            dcc.Graph(
                id='example-graph',
                figure=fig
            )
        ])

        def run_dash():
            """Запуск отобажения"""
            app.run_server(debug=True, use_reloader=False)

        thread = threading.Thread(target=run_dash)
        thread.daemon = True
        thread.start()
        webview.create_window("Интерактивный график",
                              "http://127.0.0.1:8050")
        webview.start()

    def create_figure(self):
        """Создание фигур на графике"""
        samples = np.array(self.audio.get_array_of_samples())
        sample_rate = np.fft.rfftfreq(len(samples), 1 / self.audio.frame_rate)
        fft_orig = np.abs(np.fft.rfft(samples))
        filtered_audio = self.execute_filtration()
        filtered_samples = np.array(filtered_audio.get_array_of_samples())
        fft_filtered = np.abs(np.fft.rfft(filtered_samples))

        figure = go.Figure()
        self.set_trace(figure, sample_rate, consts["amplitude"], fft_orig)
        self.set_trace(figure, sample_rate, consts["amplitude"], fft_filtered)
        figure.update_layout(
            title='Frequency Response',
            xaxis=dict(
                title='Frequency (Hz)',
                type='log',
                range=[np.log10(consts["amplitude"]),
                       np.log10(max(sample_rate))]
            ),
            yaxis=dict(title='Amplitude (dB)'),
            legend=dict(x=0, y=1)
        )
        return figure

    @staticmethod
    def set_trace(figure, sample_rate, amplitude_level, fft):
        """Добавление фигуры на график"""
        figure.add_trace(go.Scatter(
            x=sample_rate,
            y=amplitude_level * np.log10(fft),
            mode='lines',
            name='Filtered',
            line=dict(color='red')
        ))

    def execute_filtration(self):
        """Осуществление фильтрации"""
        filtered_audio = self.apply_filters([
            (consts['low_rate_start'], consts['middle_rate_start'],
             self.low_slider.get() / consts["coefficient_normalization"]),
            (consts['middle_rate_start'], consts['high_rate_start'],
             self.mid_slider.get() / consts["coefficient_normalization"]),
            (consts['high_rate_start'], consts['high_rate_end'],
             self.high_slider.get() / consts["coefficient_normalization"])
        ])
        return filtered_audio

    def visualizing_equalizer(self):
        root = tk.Tk()
        root.title("Эквалайзер")
        frame = tk.Frame(root)
        frame.pack(padx=10, pady=10)
        tk.Button(frame, text="Сохранить файл", command=self.save_file).grid(
            row=0, column=1, padx=5, pady=5)
        tk.Button(frame, text="Обновить график",
                  command=self.update_plot).grid(row=0, column=2, padx=5,
                                                 pady=5)
        self.low_slider = tk.Scale(root, from_=-10, to=10,
                                   orient=tk.HORIZONTAL, label="Низкие "
                                                               "частоты")
        self.low_slider.pack(fill=tk.X, padx=10)
        self.mid_slider = tk.Scale(root, from_=-10, to=10,
                                   orient=tk.HORIZONTAL, label="Средние "
                                                               "частоты")
        self.mid_slider.pack(fill=tk.X, padx=10)
        self.high_slider = tk.Scale(root, from_=-10, to=10,
                                    orient=tk.HORIZONTAL,
                                    label="Высокие частоты")
        self.high_slider.pack(fill=tk.X, padx=10)
        root.mainloop()
