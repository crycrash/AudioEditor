import os
import struct


class Audiofile:
    stHeaderFields = {'ChunkSize': 0, 'Format': '',
                      'Subchunk1Size': 0, 'AudioFormat': 0,
                      'NumChannels': 0, 'SampleRate': 0,
                      'ByteRate': 0, 'BlockAlign': 0,
                      'BitsPerSample': 0, 'Filename': '',
                      'Subchunk2Id': 0, 'SizeSec': 0}

    def __init__(self, path):
        self.path = path
        with open(self.path, 'rb') as wav_in:
            self.header = wav_in.read(44)
            wav_in.seek(44, os.SEEK_CUR)

            self.audio_data = wav_in.read()
            if (self.header[0:4] != b'RIFF') or \
                    (self.header[12:16] != b'fmt '):
                raise Exception("Not valid")

    def take_header_config(self):
        """Парсинг заголовка wav и высчитывание длины аудио в секундах"""
        self.stHeaderFields['ChunkSize'] = struct.unpack('<L', self.header[4:8])[0]
        self.stHeaderFields['Format'] = self.header[8:12]
        self.stHeaderFields['Subchunk1Size'] = struct.unpack('<L', self.header[16:20])[0]
        self.stHeaderFields['AudioFormat'] = struct.unpack('<H', self.header[20:22])[0]
        self.stHeaderFields['NumChannels'] = struct.unpack('<H', self.header[22:24])[0]
        self.stHeaderFields['SampleRate'] = struct.unpack('<L', self.header[24:28])[0]
        self.stHeaderFields['ByteRate'] = struct.unpack('<L', self.header[28:32])[0]
        self.stHeaderFields['BlockAlign'] = struct.unpack('<H', self.header[32:34])[0]
        self.stHeaderFields['BitsPerSample'] = struct.unpack('<H', self.header[34:36])[0]
        self.stHeaderFields['Subchunk2Id'] = struct.unpack('<L', self.header[36:40])[0]
        self.stHeaderFields['Subchunk2Size'] = struct.unpack('<L', self.header[40:44])[0]
        self.stHeaderFields['SizeSec'] = self.stHeaderFields['Subchunk2Size'] / (
                    self.stHeaderFields['BitsPerSample'] / 8) / self.stHeaderFields['SampleRate'] / self.stHeaderFields[
                                             'NumChannels']
        print(self.stHeaderFields['SizeSec'])

    def crop_file(self, start_point, end_point):
        """Обрезка файла по указанным секундам"""
        if start_point > self.stHeaderFields['SizeSec'] or end_point > self.stHeaderFields['SizeSec']:
            raise Exception('You have gone beyond the allowed length')

        count = len(self.audio_data)//self.stHeaderFields['SizeSec']
        self.audio_data = self.audio_data[int(start_point*count):int(end_point*count)]
        self.stHeaderFields['Subchunk2Size'] = self.stHeaderFields['Subchunk2Size']//2
        self.stHeaderFields['ChunkSize'] = self.stHeaderFields['Subchunk2Size'] + 36
        self.header = self.header.replace(self.header[40:44], struct.pack('<L', self.stHeaderFields['Subchunk2Size']))
        self.header = self.header.replace(self.header[4:8], struct.pack('<L', self.stHeaderFields['ChunkSize']))
        self.stHeaderFields['SizeSec'] = self.stHeaderFields['SizeSec']//2
        f = open(self.path, 'w+')
        f.seek(0)
        f.close()
        with open(self.path, 'wb') as wav_out:
            wav_out.write(self.header)
            wav_out.write(self.audio_data)
