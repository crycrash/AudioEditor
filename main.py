import sys
from audio import Audiofile


def main():
    if len(sys.argv) == 3:
        if sys.argv[2] == "save":
            a = Audiofile(sys.argv[1])
            print(a.take_header_config())
            print('ALL right')


if __name__ == "__main__":
    main()
