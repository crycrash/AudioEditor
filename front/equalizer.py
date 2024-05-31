import tkinter as tk
from pydub import AudioSegment
import numpy as np
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt


class Equalizer:
    def __init__(self, path_audio, format_audio):
        self.low_slider = None
        self.mid_slider = None
        self.high_slider = None
        self.audio = None
        self.path = path_audio
        self.format = format_audio
        self.open_audio()

    def open_audio(self):
        if self.format == 'wav':
            self.audio = AudioSegment.from_wav(self.path)
        else:
            self.audio = AudioSegment.from_mp3(self.path)

    @staticmethod
    def butter_bandpass(low_cut, high_cut, sampling_rate, order=5):
        """Возвращает коэфициенты фильтра"""
        normalization = 0.5
        nyquist_frequency = normalization * sampling_rate
        low_normalization = low_cut / nyquist_frequency
        high_normalization = high_cut / nyquist_frequency
        if high_normalization >= 1.0:
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
            if not np.any(np.isnan(filtered)):
                filtered_samples += gain * filtered
        low_limit = -32768
        upper_limit = 32767
        filtered_samples = np.clip(filtered_samples, low_limit, upper_limit)
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
                (20, 200, self.low_slider.get() / 10),
                (200, 2000, self.mid_slider.get() / 10),
                (2000, 20000, self.high_slider.get() / 10)
            ])
            output_audio.export(self.path, format="mp3")

    def update_plot(self):
        """Обновление графика"""
        if self.audio is not None:
            plt.figure(figsize=(10, 4))
            samples = np.array(self.audio.get_array_of_samples())
            sample_rate = np.fft.rfftfreq(len(samples),
                                          1 / self.audio.frame_rate)
            fft_orig = np.abs(np.fft.rfft(samples))
            amplitude_level = 20
            plt.plot(sample_rate, amplitude_level * np.log10(fft_orig),
                     label='Original', alpha=0.7)
            filtered_audio = self.execute_filtration()
            filtered_samples = np.array(filtered_audio.get_array_of_samples())
            fft_filtered = np.abs(np.fft.rfft(filtered_samples))
            plt.plot(sample_rate, amplitude_level * np.log10(fft_filtered),
                     label='Filtered', alpha=0.7)
            plt.xscale('log')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Amplitude (dB)')
            plt.legend()
            plt.title("Frequency Response")
            plt.show()

    def execute_filtration(self):
        """Осуществление фильтрации"""
        low_rate_start = 20
        middle_rate_start = 200
        high_rate_start = 2000
        high_rate_end = 20000
        coefficient_normalization = 10
        filtered_audio = self.apply_filters([
            (low_rate_start, middle_rate_start, self.low_slider.get() /
             coefficient_normalization),
            (middle_rate_start, high_rate_start, self.mid_slider.get() /
             coefficient_normalization),
            (high_rate_end, high_rate_end, self.high_slider.get() /
             coefficient_normalization)
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
