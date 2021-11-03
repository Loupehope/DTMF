from Processing.Generator import *
from IO.Write import *


if __name__ == '__main__':
    write_file_path = "/Users/vladsuhomlinov/DTMF/sound.wav"

    numbers = '123456789ABCD'
    symbols = Generator.parse_and_generate(numbers)

    Writer.write(write_file_path, symbols)

    print('Успех!')
