from Processing.Generator import *
from IO.Write import *
from Drivers.SpecInfoDisplayDriver import *

import tkinter as tk


if __name__ == '__main__':
    # Устанавливаем окно и обьект графиков
    window = tk.Tk()
    window.title("Методы обработки экспериментальных данных")
    display_model = SpecInfoDisplayDriver(window)

    # ---------------
    # Подсчеты
    write_file_path = "/Users/vladsuhomlinov/DTMF/sound.wav"

    numbers = '1'
    symbols = Generator.generate_from(numbers, 0.1)

    Writer.write(write_file_path, symbols)

    # ---------------
    # Графики

    from scipy.io.wavfile import read

    data_y = read(write_file_path)[1][0:1024]
    data_x = []

    for i in range(len(data_y)):
        data_x.append(i)

    display_model.plot([data_x, data_y])

    # Запускаем
    display_model.display()
    window.mainloop()

    print('Успех!')
