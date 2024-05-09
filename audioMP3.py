from parseMP3 import AudioFrameMp3


class Audiofile:

    def __init__(self, path):
        self.path = path
        self.audio = AudioFrameMp3(path)
        self.audio_data = self.audio.return_audio_data()
        self.headers = self.audio.all_headers
        self.sizes = self.audio.all_sizes
        self.tag = self.audio.tag
        self.count = self.audio.count
        self.length = self.audio.size

    def output_erase(self, path, start, finish, index):
        # перенести  в общий доступ
        new_data = b''
        self.path = path
        with open(path, 'wb') as wav_out:
            wav_out.write(self.tag)
            for i in range(start, finish + 1):
                new_data += self.headers[i]
                wav_out.write(self.headers[i])
                data = self.audio_data[index + 4:index + self.sizes[i]]
                new_data += data
                wav_out.write(data)
                index += self.sizes[i]
        return new_data

    def output_splice(self, path, start, index, other):
        # перенести  в общий доступ
        new_data = b''
        self.path = path
        with open(path, 'wb') as wav_out:
            wav_out.write(self.tag)
            for i in range(0, start):
                new_data += self.headers[i]
                wav_out.write(self.headers[i])
                data = self.audio_data[index + 4:index + self.sizes[i]]
                new_data += data
                wav_out.write(data)
                index += self.sizes[i]

            prev_index = index
            index = 0
            for i in range(0, other.count):
                new_data += other.headers[i]
                wav_out.write(other.headers[i])
                data = other.raw_data[index + 4:index + other.sizes[i]]
                new_data += data
                wav_out.write(data)
                index += other.sizes[i]
            for i in range(start, self.count):
                new_data += self.headers[i]
                wav_out.write(self.headers[i])
                data = self.audio_data[prev_index + 4:prev_index + self.sizes[i]]
                new_data += data
                wav_out.write(data)
                prev_index += self.sizes[i]

        return new_data

    def count_index(self, num):
        index = 0
        for i in range(num):
            index += self.sizes[i]
        return index

    def crop_audio(self, path, start_point, end_point):
        """Обрезка файла по указанным секундам"""
        if (start_point > self.length or end_point >
                self.length):
            raise Exception('You have gone beyond the allowed length')

        index = self.count_index(start_point)
        count_temp = self.count // self.length
        count_start = int(start_point * count_temp)
        count_finish = int(end_point * count_temp)

        new_data = self.output_erase(path, count_start, count_finish, index)
        self.audio_data = new_data
        self.headers = self.headers[count_start:count_finish]
        self.sizes = self.sizes[count_start:count_finish]
        self.count = count_finish - count_start
        print(self.count)
        self.length = end_point - start_point

    def splice_audio(self, path, other, start_point):
        """Вставка одного файла в другой"""
        if start_point > int(self.length):
            raise Exception('You have gone beyond the allowed length')
        if isinstance(other, Audiofile):
            count_temp = self.count // self.length
            #print(count_temp)
            count_start = int(start_point * count_temp)
            print(count_start)

            new_data = self.output_splice(path, count_start,
                                          0, other)
            self.audio_data = new_data
            self.headers = (self.headers[:int(count_start)] + other.headers +
                            self.headers[int(count_start):])
            self.sizes = (self.sizes[:int(count_start)] + other.headers +
                          self.sizes[int(count_start):])
            self.count = self.count + other.count
            self.length += other.length
        else:
            raise Exception('Что то пошло не так')


a = Audiofile('/Users/milana/Downloads/sample-15s.mp3')
a.crop_audio('/Users/milana/Downloads/sample-152s.mp3', 0, 8)
b = Audiofile('/Users/milana/Downloads/sample-9s.mp3')
a.splice_audio('/Users/milana/Downloads/splice12.mp3', b, 5)
