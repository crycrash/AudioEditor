from parseMP3 import AudioFrameMp3 as frame_header


class Audiofile:

    def __init__(self, path):
        """"Инициализация аудио фрагмента"""
        self.path = path
        self.audio_frame = frame_header(path)
        self.audio = self.audio_frame.return_audio_data()
        self.audio_data = self.audio.raw_data

    def output_files(self, path):
        """"Вывод в файл"""
        with open(path, 'wb') as wav_out:
            wav_out.write(self.audio_data)

    def crop_audio(self, path, start_point, end_point):
        """Обрезка файла по указанным секундам"""
        if (start_point > self.audio.size or end_point >
                self.audio.size):
            raise Exception('You have gone beyond the allowed length')
        frame_start = int(len(self.audio_data) // self.audio.size)
        frame_end = frame_start * end_point
        frame_start = frame_start * start_point
        new_data = self.audio_data[frame_start:frame_end]
        self.audio_data = new_data
        self.output_files(path)
        self.audio.size = end_point - start_point

    def splice_audio(self, path, other, start_point):
        """Вставка одного файла в другой"""
        if start_point > int(self.audio.size):
            raise Exception('You have gone beyond the allowed length')
        frame_start = int(len(self.audio_data) // self.audio.size)
        frame_start = frame_start * start_point
        insert_data = other.audio_data
        output_data = self.audio_data[:frame_start] + insert_data + self.audio_data[
                                                               frame_start:]
        self.audio_data = output_data
        self.output_files(path)
        self.audio.size += other.audio.size



a = Audiofile('/Users/milana/Downloads/sample4.mp3')
a.crop_audio('/Users/milana/Downloads/gitara1.mp3', 4, 10)
b = Audiofile('/Users/milana/Downloads/sample-9s.mp3')
b.splice_audio('/Users/milana/Downloads/git1.mp3', a, 3)
