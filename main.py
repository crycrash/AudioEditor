import argparse

from audioWav import Audiofile

with open('/Users/milana/Downloads/sample312.mp3', 'rb') as wav_in:
    raw_data = wav_in.read()
frame_start = (len(raw_data) / (
                128 *
                1000)) * 8
print(frame_start)
frame_start = int(len(raw_data) // frame_start)
print(frame_start)
frame_end = frame_start*20
print(frame_end)
frame_start = frame_start*9
print(frame_start)

    # Записываем обрезанные данные в новый файл
with open('/Users/milana/Downloads/gitara2.mp3', 'wb') as f:
        f.write(raw_data[frame_start:frame_end])

def insert_mp3(input_file, insert_file, output_file, start_time):
    with open(input_file, 'rb') as f:
        input_data = f.read()

    with open(insert_file, 'rb') as f:
        insert_data = f.read()

    frame_start = (len(input_data) / (
            128 *
            1000)) * 8
    print(frame_start)
    frame_start = int(len(input_data) // frame_start)
    frame_start = frame_start * start_time

    # Вставляем данные нового файла в обрезанный файл
    output_data = input_data[:frame_start] + insert_data + input_data[frame_start:]

    # Записываем результат в новый файл
    with open(output_file, 'wb') as f:
        f.write(output_data)

# Пример использования:
input_file = '/Users/milana/Downloads/sample-15s.mp3'
insert_file = '/Users/milana/Downloads/gitara2.mp3'
output_file = '/Users/milana/Downloads/sam-23445s.mp3'
start_time = 5  # начало вставки в секундах

insert_mp3(input_file, insert_file, output_file, start_time)
