import argparse

from audioWav import Audiofile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['save', 'erase', 'splice',
                                            'speed', 'stop'], help='Команда')

    example = None
    while True:
        command = input("Введите команду (save, read, erase, splice, speed): ")
        if command == 'save':
            filename = input("Введите название файла для сохранения: ")
            example = Audiofile(filename)
            example.take_header_config()
        elif command == 'erase':
            start, finish = [int(x) for x in input("Введите координаты обрезки"
                                                   " ").split()]
            if example is not None:
                example.crop_audio(start, finish)
            else:
                raise Exception("Произведите сохранение файла")
        elif command == 'splice':
            filename = input("Введите название файла с которым будет "
                             "склейка:")
            time = input("Введите время в которое хотите вставить :* ")
            other = Audiofile(filename)
            other.take_header_config()
            if other is not None and example is not None:
                example.splice_audio(other, int(time))
            else:
                raise Exception("Произведите сохранение файла")
        elif command == 'speed':
            speed = input('Введите коэфициент для замедления/ускорения аудио')
            if example is not None:
                example.speed_multiplying(float(speed))
            else:
                raise Exception("Произведите сохранение файла")
        elif command == 'stop':
            print("Программа завершена")
            break
        else:
            print("Некорректная команда")


if __name__ == "__main__":
    main()
