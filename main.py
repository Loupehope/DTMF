from IO.Write import *
from IO.Reader import *

from Processing.Generator import *
from Processing.Detector import *
from Processing.Goertzel import *

from Drivers.SpecInfoDisplayDriver import *

import tkinter as tk


if __name__ == '__main__':
    # Устанавливаем окно и обьект графиков
    # window = tk.Tk()
    # window.title("Методы обработки экспериментальных данных")
    # display_model = SpecInfoDisplayDriver(window)

    # ---------------
    # Данные на входе
    file_path = "/Users/vladsuhomlinov/DTMF/sound.wav"
    numbers = '123456789abcd*'

    # ---------------
    # Записываем
    symbols = Generator.generate_from(numbers, .25)
    Writer.write(file_path, symbols)

    # ---------------
    # Считываем
    rate, data = Reader.read(file_path)
    detected = Detector.detect(rate, data)

    print("Распознано для " + numbers + ": " + detected)

    # Запускаем
    # display_model.display()
    # window.mainloop()

    print('Успех!')
