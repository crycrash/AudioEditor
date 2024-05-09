import os
import struct


class Audiofile:

    def __init__(self, path):
        self.path = path
        with open(self.path, 'rb') as wav_in:
            self.header = wav_in.read(44)
            wav_in.seek(44, os.SEEK_CUR)

            self.audio_data = wav_in.read()
            self.stHeaderFields = {'ChunkSize': 0, 'Format': '',
                                   'Subchunk1Size': 0, 'AudioFormat': 0,
                                   'NumChannels': 0, 'SampleRate': 0,
                                   'ByteRate': 0, 'BlockAlign': 0,
                                   'BitsPerSample': 0, 'Filename': '',
                                   'Subchunk2Id': 0, 'SizeSec': 0}
            if (self.header[0:4] != b'RIFF') or \
                    (self.header[12:16] != b'fmt '):
                raise Exception("Not valid")

    def output_in_file(self):
        #перенести  в общий доступ
        f = open(self.path, 'w+')
        f.seek(0)
        f.close()
        with open(self.path, 'wb') as wav_out:
            wav_out.write(self.header)
            wav_out.write(self.audio_data)
        with open("ex.txt", 'wb') as wav_out:
            wav_out.write(self.audio_data)

    def take_header_config(self):
        """Парсинг заголовка wav и высчитывание длины аудио в секундах"""
        self.stHeaderFields['ChunkSize'] = struct.unpack('<L',
                                                         self.header[4:8])[0]
        print(self.stHeaderFields['ChunkSize'])
        self.stHeaderFields['Format'] = self.header[8:12]
        print(self.stHeaderFields['Format'])
        self.stHeaderFields['Subchunk1Size'] = struct.unpack('<L',
                                                             self.header[16:20]
                                                             )[0]
        print(self.stHeaderFields['Subchunk1Size'])
        self.stHeaderFields['AudioFormat'] = struct.unpack('<H',
                                                           self.header[20:22]
                                                           )[0]
        print(self.stHeaderFields['AudioFormat'])
        self.stHeaderFields['NumChannels'] = struct.unpack('<H',
                                                           self.header[22:24]
                                                           )[0]
        print(self.stHeaderFields['NumChannels'])
        self.stHeaderFields['SampleRate'] = struct.unpack('<L',
                                                          self.header[24:28]
                                                          )[0]
        print(self.stHeaderFields['SampleRate'])
        self.stHeaderFields['ByteRate'] = struct.unpack('<L',
                                                        self.header[28:32])[0]
        print(self.stHeaderFields['ByteRate'])
        self.stHeaderFields['BlockAlign'] = struct.unpack('<H',
                                                          self.header[32:34]
                                                          )[0]
        print(self.stHeaderFields['BlockAlign'])
        self.stHeaderFields['BitsPerSample'] = struct.unpack('<H',
                                                             self.header[34:36]
                                                             )[0]
        print(self.stHeaderFields['BitsPerSample'])
        self.stHeaderFields['Subchunk2Id'] = struct.unpack('<L',
                                                           self.header[36:40]
                                                           )[0]
        print(self.stHeaderFields['Subchunk2Id'])
        self.stHeaderFields['Subchunk2Size'] = struct.unpack('<L',
                                                             self.header[40:44]
                                                             )[0]
        print(self.stHeaderFields['Subchunk2Size'])
        self.stHeaderFields['SizeSec'] = (self.stHeaderFields['Subchunk2Size']
                                          / (
                self.stHeaderFields['BitsPerSample'] / 8) /
                                          self.stHeaderFields['SampleRate']
                                          / self.stHeaderFields[
                                             'NumChannels'])

    def crop_audio(self, start_point, end_point):
        """Обрезка файла по указанным секундам"""
        if (start_point > self.stHeaderFields['SizeSec'] or end_point >
                self.stHeaderFields['SizeSec']):
            raise Exception('You have gone beyond the allowed length')

        count = len(self.audio_data) // self.stHeaderFields['SizeSec']
        self.audio_data = self.audio_data[int(start_point * count):
                                          int(end_point * count)]
        self.stHeaderFields['Subchunk2Size'] = self.stHeaderFields[
                                                   'Subchunk2Size'] // 2
        self.stHeaderFields['ChunkSize'] = self.stHeaderFields[
                                               'Subchunk2Size'] + 36
        self.header = self.header.replace(self.header[40:44],
                                          struct.pack('<L',
                                                      self.stHeaderFields
                                                      ['Subchunk2Size']))
        self.header = self.header.replace(self.header[4:8],
                                          struct.pack('<L',
                                                      self.stHeaderFields
                                                      ['ChunkSize']))
        self.stHeaderFields['SizeSec'] = self.stHeaderFields['SizeSec'] // 2
        self.output_in_file()

    def splice_audio(self, other, time):
        """Вставка одного файла в другой"""
        if time > int(self.stHeaderFields['SizeSec']):
            raise Exception('You have gone beyond the allowed length')
        if isinstance(other, Audiofile):
            count = len(self.audio_data) // self.stHeaderFields['SizeSec']
            self.audio_data = (self.audio_data[:int(time * count)] +
                               other.audio_data
                               + self.audio_data[int(time * count):])
            self.stHeaderFields['Subchunk2Size'] = (self.stHeaderFields
                                                    ['Subchunk2Size']
                                                    + other.stHeaderFields
                                                    ['Subchunk2Size'])
            self.stHeaderFields['ChunkSize'] = self.stHeaderFields[
                                                   'Subchunk2Size'] + 36
            self.header = self.header.replace(self.header[40:44],
                                              struct.pack('<L',
                                                          self.
                                                          stHeaderFields
                                                          ['Subchunk2Size']))
            self.header = self.header.replace(self.header[4:8],
                                              struct.pack('<L',
                                                          self.
                                                          stHeaderFields
                                                          ['ChunkSize']))
            self.stHeaderFields['SizeSec'] = (self.stHeaderFields['SizeSec'] +
                                              other.stHeaderFields['SizeSec'])
            self.output_in_file()
        else:
            raise Exception('Что то пошло не так')

    def speed_multiplying(self, speed):
        """Ускорение или замедление аудио дорожки"""
        self.stHeaderFields['SampleRate'] = int(self.stHeaderFields
                                                ['SampleRate'] * speed)
        self.stHeaderFields['Subchunk2Size'] = int(self.stHeaderFields
                                                   ['Subchunk2Size'] * 1
                                                   / speed)
        self.stHeaderFields['ChunkSize'] = (self.stHeaderFields[
            'Subchunk2Size'] + 36)

        self.header = self.header.replace(self.header[40:44],
                                          struct.pack('<L',
                                                      self.stHeaderFields
                                                      ['Subchunk2Size']))
        self.header = self.header.replace(self.header[4:8],
                                          struct.pack('<L',
                                                      self.stHeaderFields
                                                      ['ChunkSize']))
        self.header = self.header.replace(self.header[24:28], struct.
                                          pack('<L',
                                               self.stHeaderFields
                                               ['SampleRate']))
        self.stHeaderFields['SizeSec'] = (self.stHeaderFields['SizeSec'] * 1
                                          / speed)
        self.output_in_file()
